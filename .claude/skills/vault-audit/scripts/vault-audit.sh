#!/usr/bin/env bash
# vault-audit.sh — Obsidian vault mechanical audit
# Usage: vault-audit.sh [full|quick|module:PATH] [--staged-only] [--json]
set -eo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$VAULT_ROOT"

MODE="${1:-full}"
STAGED_ONLY=false
JSON_OUT=false
MODULE_FILTER=""

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged-only) STAGED_ONLY=true ;;
    --json) JSON_OUT=true ;;
    module:*) MODULE_FILTER="${1#module:}"; MODE="module" ;;
    *) ;;
  esac
  shift
done

if [[ "$MODE" == module:* ]]; then
  MODULE_FILTER="${MODE#module:}"
  MODE="module"
fi

STALE_KEYWORDS=(
  "Telescope1126"
  "07.Telescope1126"
  "DriverSO"
  "SupportLib"
  "LoadSettings.py"
  "CMOS285"
)

note_files() {
  if [[ "$STAGED_ONLY" == true ]]; then
    git diff --cached --name-only --diff-filter=ACMR 2>/dev/null | grep '\.md$' || true
  elif [[ -n "$MODULE_FILTER" ]]; then
    find "$MODULE_FILTER" -name '*.md' 2>/dev/null | grep -v '\.git/' || true
  else
    find A-* B-* C-* D-* E-* F-* G-* -name '*.md' 2>/dev/null || true
  fi
}

strip_code_blocks() {
  awk 'BEGIN{blk=0} /^```/{blk=!blk; next} !blk {print}'
}

normalize_target() {
  local t="$1"
  t="${t%%|*}"
  t="${t//\\|/|}"
  t="${t//\\//}"
  t="${t%.md}"
  t="${t#"${t%%[![:space:]]*}"}"
  t="${t%"${t##*[![:space:]]}"}"
  printf '%s' "$t"
}

strip_inline_code() {
  sed -E 's/`+([^`]|\\.)*`+//g'
}

extract_wikilinks() {
  local f="$1"
  strip_code_blocks < "$f" | strip_inline_code | grep -oP '\[\[[^$\][]+?\]\]' 2>/dev/null || true
}

is_valid_wikilink() {
  local target
  target="$(normalize_target "$1")"
  [[ -z "$target" ]] && return 1
  [[ "$target" == '...' || "$target" == 'expr' ]] && return 1
  [[ "$target" == *' -lt '* || "$target" == *' -gt '* || "$target" == *' -eq '* ]] && return 1
  [[ "$target" == *' && '* || "$target" == *' || '* ]] && return 1
  return 0
}

resolve_wikilink() {
  local src="$1" target="$2"
  local src_dir candidates

  is_valid_wikilink "$target" || return 1
  target="$(normalize_target "$target")"

  if [[ "$target" == *'/'* ]]; then
    candidates=("$target.md" "./$target.md")
  else
    src_dir="$(dirname "$src")"
    candidates=("$src_dir/$target.md" "./$target.md")
    while IFS= read -r f; do
      [[ -n "$f" ]] && candidates+=("$f")
    done < <(find A-* B-* C-* D-* E-* F-* G-* -name "$target.md" 2>/dev/null || true)
  fi

  for c in "${candidates[@]}"; do
    [[ -f "$c" ]] && return 0
  done
  return 1
}

P0=0 P1=0 P2=0
declare -a ISSUES=()

add_issue() {
  local sev="$1" id="$2" msg="$3"
  ISSUES+=("$sev|$id|$msg")
  case "$sev" in
    P0) P0=$((P0 + 1)) ;;
    P1) P1=$((P1 + 1)) ;;
    P2) P2=$((P2 + 1)) ;;
  esac
}

check_m1() {
  local f line target
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    while IFS= read -r line; do
      target="${line#*[[}"
      target="${target%%]]*}"
      [[ "$target" == *'$'* ]] && continue
      is_valid_wikilink "$target" || continue
      if ! resolve_wikilink "$f" "$target"; then
        add_issue P0 M1 "断链 wikilink: $f → [[$target]]"
      fi
    done < <(extract_wikilinks "$f")
  done < <(note_files | sort -u)
}

check_m2() {
  local f img
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    while IFS= read -r img; do
      [[ "$img" != picture/* ]] && continue
      [[ "$img" == picture/xxx.png ]] && continue
      if [[ ! -f "$img" ]]; then
        add_issue P0 M2 "图片断链: $f → $img"
      fi
    done < <(strip_code_blocks < "$f" | grep -oP '!\[[^\]]*\]\((picture/[^)]+)\)' 2>/dev/null \
      | sed 's/.*(\(picture\/[^)]*\)).*/\1/' || true)
  done < <(note_files | sort -u)
}

check_m3() {
  local struct=".claude/instructions/01-repo-structure.md"
  [[ ! -f "$struct" ]] && return
  local dir expected actual line
  while IFS= read -r line; do
    [[ "$line" != *"|"* ]] && continue
    dir="$(echo "$line" | grep -oP '`[^`]+`' | head -1 | tr -d '`')"
    [[ -z "$dir" || ! -d "$dir" ]] && continue
    [[ "$dir" == .* ]] && continue
    expected="$(echo "$line" | grep -oP '\|\s*\*\*[0-9]+\*\*|\|\s*[0-9]+' | grep -oP '[0-9]+' | head -1)"
    [[ -z "$expected" ]] && continue
    actual="$(find "$dir" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
    if [[ "$actual" != "$expected" ]]; then
      add_issue P1 M3 "索引漂移: $dir 文档=$actual 索引=$expected"
    fi
  done < <(grep -E '^\| `' "$struct" 2>/dev/null || true)
}

check_m5() {
  local f first
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    [[ "$f" == *README* ]] && continue
    first="$(grep -m1 '^# ' "$f" 2>/dev/null || true)"
    [[ -z "$first" ]] && continue
    if [[ ! "$first" =~ ^#\ 1\. ]]; then
      add_issue P1 M5 "首行一级标题非 # 1.: $f → $first"
    fi
  done < <(note_files | sort -u)
}

check_m6() {
  local f linenum
  while IFS= read -r f; do
    linenum="$(head -1 "$f" 2>/dev/null || true)"
    [[ "$linenum" == '---' ]] && add_issue P1 M6 "YAML frontmatter: $f"
  done < <(note_files | sort -u)
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    while IFS= read -r linenum; do
      add_issue P1 M6 "无标注代码块（开 fence）: $f:$linenum"
    done < <(awk '/^[ \t]*```[ \t]*$/ { if (!inblock) print NR; inblock=!inblock; next }
                  /^[ \t]*```/ { inblock=1; next }' "$f" 2>/dev/null || true)
  done < <(note_files | sort -u)
}

check_m7() {
  local dir
  for dir in A-*/* B-*/* C-*/* D-*/* E-*/* F-* G-*; do
    [[ ! -d "$dir" ]] && continue
    local nums=()
    while IFS= read -r f; do
      local bn n
      bn="$(basename "$f" .md)"
      n="$(echo "$bn" | grep -oP '^\d+' || true)"
      [[ -z "$n" ]] && continue
      for existing in "${nums[@]:-}"; do
        [[ "$existing" == "$n" ]] && add_issue P2 M7 "序号冲突: $dir/$bn (N=$n 重复)"
      done
      nums+=("$n")
    done < <(find "$dir" -maxdepth 1 -name '*.md' 2>/dev/null)
  done
}

check_m8() {
  local f line target resolved
  declare -A inbound outbound
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    inbound["$f"]=0
    outbound["$f"]=0
  done < <(note_files | sort -u)

  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    while IFS= read -r line; do
      target="${line#*[[}"
      target="${target%%]]*}"
      [[ "$target" == *'$'* ]] && continue
      is_valid_wikilink "$target" || continue
      outbound["$f"]=$(( ${outbound[$f]:-0} + 1 ))
      if resolve_wikilink "$f" "$target"; then
        target="$(normalize_target "$target")"
        if [[ "$target" == *'/'* ]]; then
          resolved="${target}.md"
        else
          resolved="$(find A-* B-* C-* D-* E-* F-* G-* -name "$(basename "$target").md" 2>/dev/null | head -1)"
        fi
        [[ -f "$resolved" ]] && inbound["$resolved"]=$(( ${inbound[$resolved]:-0} + 1 ))
      fi
    done < <(extract_wikilinks "$f")
  done < <(note_files | sort -u)

  for f in "${!inbound[@]}"; do
    [[ "$f" == *README* ]] && continue
    [[ "${inbound[$f]:-0}" -eq 0 && "${outbound[$f]:-0}" -eq 0 ]] && \
      add_issue P2 M8 "孤立笔记: $f (0 入链 0 出链)"
  done
}

check_m9() {
  local kw hit f
  for kw in "${STALE_KEYWORDS[@]}"; do
    while IFS= read -r hit; do
      [[ -z "$hit" ]] && continue
      f="${hit%%:*}"
      [[ "$f" == *'.claude/'* ]] && continue
      add_issue P1 M9 "陈旧关键词 '$kw': $hit"
    done < <(grep -rn "$kw" --include='*.md' A-* B-* C-* D-* E-* F-* G-* 2>/dev/null || true)
  done
}

check_m10() {
  local f
  while IFS= read -r f; do
    [[ -z "$f" || ! -f "$f" ]] && continue
    [[ "$f" == *README* ]] && continue
    while IFS= read -r _; do
      add_issue P1 M10 "表格内 wikilink 别名: $f"
    done < <(strip_code_blocks < "$f" | grep -nP '^\|[^\n]*\[\[[^|\]]+\|[^\]]+\]\]' 2>/dev/null || true)
  done < <(note_files | sort -u)
}

run_checks() {
  set +e
  check_m1
  check_m2
  check_m10
  if [[ "$MODE" == "full" ]]; then
    check_m3
    check_m5
    check_m6
    check_m7
    check_m8
    check_m9
  elif [[ "$MODE" == "quick" ]]; then
    check_m3
    check_m9
  fi
  set -e
}

run_checks

if [[ "$JSON_OUT" == true ]]; then
  echo "{"
  echo "  \"mode\": \"$MODE\","
  echo "  \"p0\": $P0, \"p1\": $P1, \"p2\": $P2,"
  echo "  \"issues\": ["
  first=true
  for item in "${ISSUES[@]}"; do
    IFS='|' read -r sev id msg <<< "$item"
    $first || echo ","
    first=false
    msg="${msg//\"/\\\"}"
    printf '    {"severity":"%s","id":"%s","message":"%s"}' "$sev" "$id" "$msg"
  done
  echo ""
  echo "  ]"
  echo "}"
else
  echo "=== vault-audit ($MODE) ==="
  echo "P0: $P0  P1: $P1  P2: $P2  合计: $((P0 + P1 + P2))"
  echo ""
  for sev in P0 P1 P2; do
    echo "--- $sev ---"
    for item in "${ISSUES[@]}"; do
      [[ "$item" == "$sev|"* ]] && echo "  ${item#*|}"
    done
    echo ""
  done
fi

[[ $P0 -gt 0 ]] && exit 2
[[ $P1 -gt 0 && "$MODE" == "quick" ]] && exit 1
exit 0
