#!/usr/bin/env python3
"""vault-audit.py — Obsidian vault mechanical audit (Python primary, stdlib only)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_VAULT = SCRIPT_DIR.parents[3]

STALE_KEYWORDS = [
    "Telescope1126", "07.Telescope1126", "DriverSO", "SupportLib", "LoadSettings.py", "CMOS285",
]

WIKILINK_RE = re.compile(r"\[\[[^$\][]+?\]\]")
IMG_RE = re.compile(r"!\[[^\]]*\]\((picture/[^)]+)\)")
TABLE_ALIAS_RE = re.compile(r"^\|[^\n]*\[\[[^|\]]+\|[^\]]+\]\]", re.M)


def strip_code_blocks(text: str) -> str:
    out, in_blk = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_blk = not in_blk
            continue
        if not in_blk:
            out.append(line)
    return "\n".join(out)


def strip_inline_code(text: str) -> str:
    return re.sub(r"`+([^`]|\\.)*`+", "", text)


def normalize_target(raw: str) -> str:
    t = raw.split("|", 1)[0].replace("\\|", "|").replace("\\", "/").strip()
    if t.endswith(".md"):
        t = t[:-3]
    return t.strip()


def is_valid_wikilink(target: str) -> bool:
    t = normalize_target(target)
    if not t or t in ("...", "expr"):
        return False
    if any(x in t for x in (" -lt ", " -gt ", " -eq ", " && ", " || ")):
        return False
    return True


def module_globs(vault: Path) -> list[Path]:
    mods = []
    for pat in ("A-*", "B-*", "C-*", "D-*", "E-*", "F-*", "G-*"):
        mods.extend(vault.glob(pat))
    return [m for m in mods if m.is_dir()]


def note_files(vault: Path, mode: str, module_filter: str, staged_only: bool) -> list[Path]:
    if staged_only:
        try:
            r = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                capture_output=True, text=True, check=False, cwd=vault,
            )
            return [vault / f for f in r.stdout.splitlines() if f.endswith(".md") and (vault / f).is_file()]
        except OSError:
            return []
    if module_filter:
        base = vault / module_filter
        return list(base.rglob("*.md")) if base.is_dir() else []
    files = []
    for mod in module_globs(vault):
        files.extend(mod.rglob("*.md"))
    return files


def resolve_wikilink(vault: Path, src: Path, target: str) -> Path | None:
    if not is_valid_wikilink(target):
        return None
    t = normalize_target(target)
    candidates: list[Path] = []
    if "/" in t:
        candidates = [vault / f"{t}.md", Path(f"{t}.md")]
    else:
        candidates = [src.parent / f"{t}.md", vault / f"{t}.md"]
        for mod in module_globs(vault):
            candidates.extend(mod.rglob(f"{t}.md"))
    for c in candidates:
        try:
            if c.is_file():
                return c.resolve()
        except OSError:
            continue
    return None


class Audit:
    def __init__(self):
        self.issues: list[tuple[str, str, str]] = []
        self.p0 = self.p1 = self.p2 = 0

    def add(self, sev: str, mid: str, msg: str):
        self.issues.append((sev, mid, msg))
        if sev == "P0":
            self.p0 += 1
        elif sev == "P1":
            self.p1 += 1
        else:
            self.p2 += 1


def check_m1(a: Audit, vault: Path, files: list[Path]):
    for f in files:
        text = strip_inline_code(strip_code_blocks(f.read_text(encoding="utf-8", errors="replace")))
        for m in WIKILINK_RE.findall(text):
            inner = m[2:-2]
            if "$" in inner:
                continue
            if not is_valid_wikilink(inner):
                continue
            if resolve_wikilink(vault, f, inner) is None:
                a.add("P0", "M1", f"断链 wikilink: {f.relative_to(vault)} → [[{inner.split('|')[0]}]]")


def check_m2(a: Audit, vault: Path, files: list[Path]):
    for f in files:
        text = strip_code_blocks(f.read_text(encoding="utf-8", errors="replace"))
        for img in IMG_RE.findall(text):
            if img == "picture/xxx.png":
                continue
            if not (vault / img).is_file():
                a.add("P0", "M2", f"图片断链: {f.relative_to(vault)} → {img}")


def check_m3(a: Audit, vault: Path):
    struct = vault / ".claude/instructions/01-repo-structure.md"
    if not struct.is_file():
        return
    for line in struct.read_text(encoding="utf-8", errors="replace").splitlines():
        if "| `" not in line:
            continue
        dm = re.search(r"`([^`]+)`", line)
        if not dm:
            continue
        d = vault / dm.group(1)
        if not d.is_dir() or dm.group(1).startswith("."):
            continue
        em = re.search(r"\|\s*\*\*(\d+)\*\*|\|\s*(\d+)", line)
        if not em:
            continue
        expected = int(em.group(1) or em.group(2))
        actual = len(list(d.glob("*.md")))
        if actual != expected:
            a.add("P1", "M3", f"索引漂移: {dm.group(1)} 文档={actual} 索引={expected}")


def check_m5(a: Audit, files: list[Path], vault: Path):
    for f in files:
        if "README" in f.name:
            continue
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                if not re.match(r"^#\s1\.", line):
                    a.add("P1", "M5", f"首行一级标题非 # 1.: {f.relative_to(vault)} → {line.strip()}")
                break


def check_m6(a: Audit, files: list[Path], vault: Path):
    fence_open = re.compile(r"^[ \t]*```[ \t]*$")
    for f in files:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        if lines and lines[0].strip() == "---":
            a.add("P1", "M6", f"YAML frontmatter: {f.relative_to(vault)}")
        in_blk = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                if fence_open.match(line) and not in_blk:
                    a.add("P1", "M6", f"无标注代码块（开 fence）: {f.relative_to(vault)}:{i}")
                in_blk = not in_blk


def check_m7(a: Audit, vault: Path):
    patterns = ["A-*/*", "B-*/*", "C-*/*", "D-*/*", "E-*/*", "F-*", "G-*"]
    for pat in patterns:
        for d in vault.glob(pat):
            if not d.is_dir():
                continue
            seen: set[str] = set()
            for md in d.glob("*.md"):
                m = re.match(r"^(\d+)", md.stem)
                if not m:
                    continue
                n = m.group(1)
                if n in seen:
                    a.add("P2", "M7", f"序号冲突: {d.relative_to(vault)}/{md.name} (N={n} 重复)")
                seen.add(n)


def check_m8(a: Audit, vault: Path, files: list[Path]):
    inbound: defaultdict[str, int] = defaultdict(int)
    outbound: defaultdict[str, int] = defaultdict(int)
    file_keys = {str(f.resolve()): f for f in files}
    for fk in file_keys:
        inbound[fk] = outbound[fk] = 0
    for f in files:
        text = strip_inline_code(strip_code_blocks(f.read_text(encoding="utf-8", errors="replace")))
        for m in WIKILINK_RE.findall(text):
            inner = m[2:-2]
            if "$" in inner or not is_valid_wikilink(inner):
                continue
            outbound[str(f.resolve())] += 1
            resolved = resolve_wikilink(vault, f, inner)
            if resolved:
                inbound[str(resolved.resolve())] += 1
    for fk, f in file_keys.items():
        if "README" in f.name:
            continue
        if inbound[fk] == 0 and outbound[fk] == 0:
            a.add("P2", "M8", f"孤立笔记: {f.relative_to(vault)} (0 入链 0 出链)")


def check_m9(a: Audit, vault: Path):
    files = note_files(vault, "full", "", False)
    for kw in STALE_KEYWORDS:
        for f in files:
            if ".claude" in f.parts:
                continue
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if kw in line:
                        a.add("P1", "M9", f"陈旧关键词 '{kw}': {f.relative_to(vault)}:{i}:{line.strip()[:80]}")
            except OSError:
                continue


def check_m10(a: Audit, files: list[Path], vault: Path):
    for f in files:
        if "README" in f.name:
            continue
        text = strip_code_blocks(f.read_text(encoding="utf-8", errors="replace"))
        if TABLE_ALIAS_RE.search(text):
            a.add("P1", "M10", f"表格内 wikilink 别名: {f.relative_to(vault)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="full", help="full|quick|module:PATH")
    ap.add_argument("--staged-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    args, rest = ap.parse_known_args()

    mode = args.mode
    module_filter = ""
    if mode.startswith("module:"):
        module_filter = mode[7:]
        mode = "module"
    for r in rest:
        if r == "--json":
            args.json = True
        elif r == "--staged-only":
            args.staged_only = True
        elif r.startswith("module:"):
            module_filter = r[7:]
            mode = "module"

    vault = DEFAULT_VAULT.resolve()
    if mode == "module" and module_filter and not (vault / module_filter).is_dir():
        print(f"vault-audit: module path not found: {module_filter}", file=sys.stderr)
        return 3

    staged = args.staged_only
    if staged:
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, cwd=vault, capture_output=True)
        except (subprocess.CalledProcessError, OSError):
            staged = False

    files = sorted(set(note_files(vault, mode, module_filter, staged)))
    a = Audit()

    check_m1(a, vault, files)
    check_m2(a, vault, files)
    check_m10(a, files, vault)
    if mode == "full":
        check_m3(a, vault)
        check_m5(a, files, vault)
        check_m6(a, files, vault)
        check_m7(a, vault)
        check_m8(a, vault, files)
        check_m9(a, vault)
    elif mode == "quick":
        check_m3(a, vault)
        check_m9(a, vault)

    if args.json:
        payload = {
            "mode": mode,
            "p0": a.p0, "p1": a.p1, "p2": a.p2,
            "issues": [{"severity": s, "id": i, "message": m} for s, i, m in a.issues],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"=== vault-audit ({mode}, python) ===")
        print(f"P0: {a.p0}  P1: {a.p1}  P2: {a.p2}  合计: {a.p0 + a.p1 + a.p2}\n")
        for sev in ("P0", "P1", "P2"):
            print(f"--- {sev} ---")
            for s, i, m in a.issues:
                if s == sev:
                    print(f"  {i}|{m}")
            print()

    if a.p0 > 0:
        return 2
    if a.p1 > 0 and mode == "quick":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
