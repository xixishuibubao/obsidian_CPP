#!/usr/bin/env bash
# vault-audit.sh — wrapper: python > bash (legacy inline)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
PY="$SCRIPT_DIR/vault-audit.py"
LEGACY="$SCRIPT_DIR/vault-audit.legacy.sh"

run_python() {
  local py=""
  if command -v python3 >/dev/null 2>&1; then py=python3
  elif command -v python >/dev/null 2>&1; then py=python
  fi
  if [[ -n "$py" && -f "$PY" ]]; then
    cd "$VAULT_ROOT"
    "$py" "$PY" "$@"
    return $?
  fi
  return 127
}

if run_python "$@"; then exit 0; fi

if [[ -f "$LEGACY" ]]; then
  bash "$LEGACY" "$@"
  exit $?
fi

echo "vault-audit: need python3 for vault-audit.py" >&2
exit 127
