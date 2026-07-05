#!/usr/bin/env python3
"""probe-toolchain.py — Tier 1 dev tool discovery (Python primary, stdlib only)."""
from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_VAULT = SCRIPT_DIR.parents[3]

TIER1_TOOLS = ("python", "node", "perl", "git", "bash")
OPTIONAL_TOOLS = ("jq",)

STALE_IGNORE = re.compile(r"WindowsApps", re.I)


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def in_path_env(exe: Path) -> bool:
    parent = str(exe.parent.resolve()).rstrip("\\/")
    for p in os.environ.get("Path", "").split(";"):
        if p.strip().rstrip("\\/") == parent:
            return True
    return False


def run_version(exe: str, *args: str) -> str | None:
    try:
        out = subprocess.run(
            [exe, *args], capture_output=True, text=True, timeout=15, check=False
        )
        text = (out.stdout or "") + (out.stderr or "")
        m = re.search(r"(\d+\.\d+\.\d+)", text)
        if m:
            return m.group(1)
        m = re.search(r"(\d+\.\d+)", text)
        if m:
            return m.group(1)
        return text.strip().lstrip("v") or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def where_exe(name: str) -> list[Path]:
    found: list[Path] = []
    w = shutil.which(name)
    if w:
        found.append(Path(w))
    if platform.system() == "Windows":
        try:
            r = subprocess.run(
                ["where.exe", name], capture_output=True, text=True, check=False
            )
            for line in r.stdout.splitlines():
                p = Path(line.strip())
                if p.is_file() and p not in found:
                    found.append(p)
        except OSError:
            pass
    return found


def dedupe_candidates(raw: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for c in raw:
        p = Path(c.get("path", ""))
        if not p.is_file():
            continue
        key = str(p.resolve()).lower()
        if key in seen:
            continue
        seen.add(key)
        c = dict(c)
        c["path"] = str(p.resolve())
        c["in_path"] = in_path_env(p)
        out.append(c)
    return out


def version_meets(ver: str | None, prefer: str | None) -> bool:
    if not prefer or not ver:
        return True
    pv = [int(x) for x in re.findall(r"\d+", prefer)[:3]]
    vv = [int(x) for x in re.findall(r"\d+", ver)[:3]]
    for i, p in enumerate(pv):
        if i >= len(vv):
            return False
        if vv[i] > p:
            return True
        if vv[i] < p:
            return False
    return True


def parse_version_key(ver: str | None) -> tuple:
    if not ver:
        return (0, 0, 0)
    parts = [int(x) for x in re.findall(r"\d+", ver)[:3]]
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def get_pin(project_pin: dict | None, global_pin: dict | None, tool: str) -> tuple[str | None, str | None]:
    if project_pin and tool in project_pin and isinstance(project_pin[tool], str):
        return project_pin[tool], "project_pin"
    if global_pin and tool in global_pin and isinstance(global_pin[tool], str):
        return global_pin[tool], "global_pin"
    return None, None


def get_prefer(project_pin: dict | None, global_pin: dict | None, tool: str) -> str | None:
    for pin in (project_pin, global_pin):
        if pin and isinstance(pin.get("prefer"), dict) and tool in pin["prefer"]:
            return str(pin["prefer"][tool])
    return None


def select_tool(
    tool: str,
    candidates: list[dict],
    missing_hint: str,
    project_pin: dict | None,
    global_pin: dict | None,
    auto_rank=None,
) -> dict:
    pin_path, pin_src = get_pin(project_pin, global_pin, tool)
    if pin_path and Path(pin_path).is_file():
        sel = {"path": str(Path(pin_path).resolve()), "source": pin_src}
        if tool == "python":
            sel["version"] = run_version(pin_path, "--version")
        elif tool == "node":
            sel["version"] = run_version(pin_path, "--version")
        elif tool == "perl":
            sel["version"] = run_version(pin_path, "-e", "print $^V")
            sel["flavor"] = perl_flavor(pin_path)
        else:
            sel["version"] = run_version(pin_path, "--version")
        return {"status": "ok", "selected": sel, "candidates": candidates, "fix_hint": None}

    cands = dedupe_candidates(candidates)
    if not cands:
        return {"status": "missing", "selected": None, "candidates": [], "fix_hint": missing_hint}

    prefer = get_prefer(project_pin, global_pin, tool)
    filtered = [c for c in cands if version_meets(c.get("version"), prefer)] or cands

    selected = auto_rank(filtered, prefer) if auto_rank else None
    if not selected and len(filtered) == 1:
        selected = filtered[0]
        selected.setdefault("source", "path")

    if not selected and len(filtered) > 1:
        if tool == "bash":
            bash_exe = [c for c in filtered if re.search(r"[\\/]bin[\\/]bash\.exe$", c["path"], re.I)]
            if len(bash_exe) == 1:
                selected = bash_exe[0]
                selected.setdefault("source", "path")
        if not selected:
            sorted_c = sorted(filtered, key=lambda c: parse_version_key(c.get("version")), reverse=True)
            top_ver = sorted_c[0].get("version")
            same = [c for c in sorted_c if c.get("version") == top_ver]
            if len(same) == 1:
                selected = same[0]
                selected.setdefault("source", "path")
            else:
                return {
                    "status": "ambiguous",
                    "selected": None,
                    "candidates": cands,
                    "fix_hint": (
                        f"Multiple {tool} candidates; pin in .claude/toolchain.local.json "
                        "(see .claude/toolchain.example.json)"
                    ),
                }

    if selected:
        status = "ok" if selected.get("in_path") else "not_in_path"
        hint = None
        if status == "not_in_path":
            hint = f"Found but not in PATH. Run: $env:Path += ';{Path(selected['path']).parent}'"
        sel = {k: v for k, v in selected.items() if k in ("path", "version", "source", "flavor")}
        return {"status": status, "selected": sel, "candidates": cands, "fix_hint": hint}

    return {"status": "missing", "selected": None, "candidates": cands, "fix_hint": missing_hint}


def perl_flavor(path: str) -> str:
    p = path.replace("\\", "/")
    if "Strawberry" in p:
        return "strawberry"
    if re.search(r"Git[/\\]usr", p, re.I):
        return "git"
    if "ActiveState" in p:
        return "activestate"
    return "unknown"


def perl_auto_rank(filtered: list[dict], _prefer: str | None) -> dict | None:
    straw = [c for c in filtered if c.get("flavor") == "strawberry"]
    if straw:
        return max(straw, key=lambda c: parse_version_key(c.get("version")))
    git = [c for c in filtered if c.get("flavor") == "git"]
    if git:
        return git[0]
    if filtered:
        return max(filtered, key=lambda c: parse_version_key(c.get("version")))
    return None


def probe_python(project_pin, global_pin) -> dict:
    cands: list[dict] = []
    try:
        r = subprocess.run(["py", "-0p"], capture_output=True, text=True, timeout=20, check=False)
        for line in r.stdout.splitlines():
            m = re.match(r"\s*-V:\s*(\S+)\s+(.*)$", line)
            if m and Path(m.group(2).strip()).is_file():
                p = m.group(2).strip()
                cands.append({"path": p, "version": run_version(p, "--version"), "source": "py_launcher"})
    except OSError:
        pass
    for name in ("python", "python3"):
        for p in where_exe(name):
            cands.append({"path": str(p), "version": run_version(str(p), "--version"), "source": "path"})
    globs = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python*\python.exe"),
        os.path.expandvars(r"%USERPROFILE%\miniconda3\python.exe"),
        os.path.expandvars(r"%USERPROFILE%\anaconda3\python.exe"),
        r"C:\Python*\python.exe",
    ]
    for pat in globs:
        for p in glob.glob(pat):
            cands.append({"path": p, "version": run_version(p, "--version"), "source": "common_path"})
    cands = [c for c in cands if not (STALE_IGNORE.search(c["path"]) and not c.get("version"))]
    return select_tool(
        "python", cands,
        "Python not found. Install: https://www.python.org/downloads/ or choco install python",
        project_pin, global_pin,
    )


def probe_node(project_pin, global_pin) -> dict:
    cands = []
    for p in where_exe("node"):
        cands.append({"path": str(p), "version": run_version(str(p), "--version"), "source": "path"})
    for p in [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "nodejs" / "node.exe",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "nodejs" / "node.exe",
    ]:
        if p.is_file():
            cands.append({"path": str(p), "version": run_version(str(p), "--version"), "source": "common_path"})
    nvm = os.environ.get("NVM_HOME")
    if nvm:
        np = Path(nvm) / "nodejs" / "node.exe"
        if np.is_file():
            cands.append({"path": str(np), "version": run_version(str(np), "--version"), "source": "common_path"})
    return select_tool(
        "node", cands,
        "Node.js not found. Install: https://nodejs.org/ or choco install nodejs-lts",
        project_pin, global_pin,
    )


def probe_simple(tool: str, names: tuple[str, ...], common_paths: list[Path], missing_hint: str,
                 project_pin, global_pin, version_args=("--version",)) -> dict:
    cands = []
    for name in names:
        for p in where_exe(name):
            cands.append({"path": str(p), "version": run_version(str(p), *version_args), "source": "path"})
    for p in common_paths:
        if p.is_file():
            cands.append({"path": str(p), "version": run_version(str(p), *version_args), "source": "common_path"})
    return select_tool(tool, cands, missing_hint, project_pin, global_pin)


def probe_perl(project_pin, global_pin) -> dict:
    cands = []
    for p in where_exe("perl"):
        ps = str(p)
        cands.append({"path": ps, "version": run_version(ps, "-e", "print $^V"), "source": "path", "flavor": perl_flavor(ps)})
    paths = [
        Path(r"C:\Strawberry\perl\bin\perl.exe"),
        Path.home() / "Strawberry" / "perl" / "bin" / "perl.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "usr" / "bin" / "perl.exe",
    ]
    for p in paths:
        if p.is_file():
            ps = str(p)
            cands.append({"path": ps, "version": run_version(ps, "-e", "print $^V"), "source": "common_path", "flavor": perl_flavor(ps)})
    result = select_tool(
        "perl", cands,
        "Perl not found. Install Strawberry Perl: https://strawberryperl.com/ or choco install strawberryperl",
        project_pin, global_pin, auto_rank=perl_auto_rank,
    )
    if result.get("selected", {}) and result["selected"].get("flavor") == "git":
        result["status"] = "ok"
        result["fix_hint"] = "Git bundled Perl; install Strawberry Perl and pin in toolchain.local.json if modules missing."
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Probe Tier 1 dev tools")
    ap.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT)
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()
    vault = args.vault_root.resolve()
    os.chdir(vault)

    global_pin = load_json(Path.home() / ".claude" / "toolchain.local.json")
    project_pin = load_json(vault / ".claude" / "toolchain.local.json")

    pf = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    tools = {
        "python": probe_python(project_pin, global_pin),
        "node": probe_node(project_pin, global_pin),
        "git": probe_simple("git", ("git",), [
            pf / "Git" / "cmd" / "git.exe",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "Git" / "cmd" / "git.exe",
        ], "Git not found. Install: https://git-scm.com/download/win", project_pin, global_pin),
        "bash": probe_simple("bash", ("bash",), [
            pf / "Git" / "bin" / "bash.exe",
            pf / "Git" / "git-bash.exe",
        ], "Git Bash not found. Install Git for Windows: https://git-scm.com/download/win", project_pin, global_pin),
        "jq": probe_simple("jq", ("jq",), [
            pf / "Git" / "usr" / "bin" / "jq.exe",
        ], "jq not found. May ship with Git for Windows; or choco install jq", project_pin, global_pin),
        "perl": probe_perl(project_pin, global_pin),
    }

    for name in TIER1_TOOLS:
        tools[name]["tier"] = "required"
    for name in OPTIONAL_TOOLS:
        tools[name]["tier"] = "optional"

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "machine": {"os": platform.system().lower(), "arch": platform.machine()},
        "tools": tools,
    }
    out = vault / ".claude" / "toolchain.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    has_missing = any(tools[n]["status"] == "missing" for n in TIER1_TOOLS)
    has_ambiguous = any(tools[n]["status"] == "ambiguous" for n in TIER1_TOOLS)

    def print_tool(name: str) -> None:
        t = tools[name]
        sel = t.get("selected") or {}
        ver = sel.get("version") or "-"
        extra = f" ({sel['flavor']})" if sel.get("flavor") else ""
        print(f"  {name:<6} {t['status']:<10} {ver}{extra}")
        if sel.get("path"):
            print(f"         {sel['path']}")
        if t.get("fix_hint"):
            print(f"         hint: {t['fix_hint']}")

    if not args.json_only:
        print("=== probe-toolchain (python) ===\n")
        for name in TIER1_TOOLS:
            print_tool(name)
        if OPTIONAL_TOOLS:
            print("\n  --- optional (ignored for exit code) ---")
            for name in OPTIONAL_TOOLS:
                print_tool(name)
        print(f"\n  报告: {out}")

    if has_ambiguous:
        return 2
    if has_missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
