#!/usr/bin/env bash
# probe-toolchain.sh — wrapper: python > bash fallback > powershell
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
PY="$SCRIPT_DIR/probe-toolchain.py"
PS1="$SCRIPT_DIR/probe-toolchain.ps1"

run_python() {
  local py=""
  if command -v python3 >/dev/null 2>&1; then py=python3
  elif command -v python >/dev/null 2>&1; then py=python
  fi
  if [[ -n "$py" && -f "$PY" ]]; then
    "$py" "$PY" --vault-root "$VAULT_ROOT" "$@"
    return $?
  fi
  return 127
}

if run_python "$@"; then exit 0; fi
rc=$?
if [[ "$rc" -le 2 ]]; then exit "$rc"; fi

if command -v powershell.exe >/dev/null 2>&1 && [[ -f "$PS1" ]]; then
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PS1" -VaultRoot "$VAULT_ROOT" "$@"
  exit $?
fi

echo "probe-toolchain: need python3 or powershell" >&2
exit 127
