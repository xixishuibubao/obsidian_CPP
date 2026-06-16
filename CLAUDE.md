# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An **Obsidian vault** containing personal study notes on C/C++, systems programming, Linux, and related engineering topics. Organized as numbered markdown files by subject area.

This is **not a code project** — there are no build systems, no tests, and no compilable source. It is a knowledge base for reference and review.

English readers see [README_EN.md](readme/README_EN.md).

## Quick Reference

| 项目 | 规则 |
|------|------|
| **笔记引用** | Obsidian wikilink `[[文件名\|显示文字]]` |
| **标题格式** | `# N.` / `## N.N` 强制编号，`###` 起可选 |
| **Frontmatter** | 不使用 YAML frontmatter 或 tags |
| **图片引用** | `![描述](picture/文件名.png)` |
| **编码** | 中文内容优先 Bash，乱码时回退 PowerShell 并设 `LC_ALL=C.UTF-8` |
| **空目录占位** | 使用 `.gitkeep` 文件占位 |

## Common Workflows

### Create a New Note
1. **Place** in the appropriate subdirectory (e.g., `C-Linux生态/01.Linux环境/`)
2. **Name** as `N. Title.md` — N is the next available sort number within that subdirectory; internal title always starts at `# 1.`
3. **Content** follows [02-note-conventions.md](.claude/instructions/02-note-conventions.md): fenced code blocks + language annotation, wikilinks to related notes, bilingual (English terms + Chinese explanation)
4. **Images** go to `picture/`; reference as `![desc](picture/file.png)`
5. **Commit** with `docs(目录): 新增了什么内容`（description 用简体中文）

### Rename / Move a Note
1. Update the file name and `# 1.` title header inside it
2. Update all `[[old-name]]` wikilinks across the vault:
   ```bash
   grep -roP '\[\[old-name(?:\|.*?)?\]\]' . --include='*.md' | grep -v '\.git/'
   ```
3. **Wikilink 更新要点**：
   - 目标路径不含 `.md` 后缀（`[[file]]` 而非 `[[file.md]]`）
   - 跨模块引用使用 vault 相对路径 `[[模块-名称/子目录/文件名]]`
4. Fix image paths in the moved note if the section number changed
5. Commit with `refactor(目录): 描述`

### Maintain Directories
- After creating/removing a directory, run the `.gitkeep` hook:
  ```powershell
  powershell -File .git\hooks\auto-gitkeep.ps1
  ```
  > 脚本不存在时，手动补齐：`Get-ChildItem -Directory -Recurse | Where-Object { (Get-ChildItem $_.FullName -File -Exclude '.gitkeep').Count -eq 0 } | ForEach-Object { New-Item -ItemType File -Path (Join-Path $_.FullName '.gitkeep') -Force }`
  > `.git\hooks\auto-gitkeep.ps1` 依赖本机 hooks 脚本；其他机器首次运行会因脚本不存在而回退到此内联命令
- Check repo state: `git status` / `git log --oneline -5`

### Squash Before Push
```bash
# 交互式 rebase（推荐）
git rebase -i HEAD~N

# 或 soft reset（仅保留一版）
git reset --soft HEAD~N && git commit -m "type(scope): description"
```

详见 [03-git-workflow.md](.claude/instructions/03-git-workflow.md)。

### Pre-commit 自检
提交前依序执行以下步骤：

**Step 1 — 换行符统一**（避免仅换行符改动的提交）：
```bash
git add --renormalize .
```

**Step 2 — 完整性检查**，发现问题先修复再提交：
```bash
# 1) 标题格式
grep -rnP '^# \d' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'README' | grep -v '99\.'
# 2) YAML frontmatter
grep -rlnP '^---$' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'CLAUDE.md'
# 3) 无标注代码块
grep -rnP '^\x60\x60\x60\s*$' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/'
# 4) 增量变更文件的完整审查见下文
```

增量审查细则见 [06-continuous-review.md](.claude/instructions/06-continuous-review.md)。

## Useful Commands

All paths relative to vault root.

### 📋 统计
```bash
# 近期变更
git log --oneline --name-status -10

# 各模块笔记数（递归，含子目录）
for d in A-*/ B-*/ C-*/ D-*/ E-*/ F-*/ G-*/; do count=$(find "$d" -name '*.md' | wc -l); echo "${d%/} → $count 篇"; done

```

### ✅ 完整性检查
```bash
# 标题格式（1 级标题应全部为 # N. 格式）
grep -rnP '^# \d' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'README' | grep -v '99\.'

# 可能断裂的 wikilinks（排除 shell [[ 条件）
grep -roP '\[\[[^$\][]+?\]\]' . --include='*.md' | grep -v '\.git/' | sort -u

# 引用不存在的图片
grep -roP '\!\[.*?\]\(picture/[^)]+\)' . --include='*.md' | grep -v '\.git/'
```

### 🔧 维护
```bash
git add --renormalize .                           # 批量修复 LF → CRLF
powershell .git\hooks\auto-gitkeep.ps1            # 更新 .gitkeep
```

## Directory Overview

完整结构与笔记计数见 [01-repo-structure.md](.claude/instructions/01-repo-structure.md)。

## Key Rules

1. **每次改动后本地 commit，推远端前 squash** — 保持远端 log 清晰
2. **Commit 用 Conventional Commits 格式**：`type(scope): description`，内容优先用简体中文。description 须简述具体改动点，不得过度概括导致信息丢失（如"修复若干问题"不合理，应列出各文件的具体变更原因）
3. **笔记使用标准 Markdown**，无 YAML frontmatter，无 tags
4. **终端优先用 Bash**，中文乱码时回退 PowerShell
5. **目录变更后运行 `.gitkeep` hook**
6. **commit 前必须统一换行符** — 运行 `git add --renormalize .` 使 CRLF/LF 与 `.gitattributes` 一致，避免仅换行符改动的提交
7. **本文件保持简洁**（100~130 行），接近上限时拆分至 `.claude/instructions/` 子文件
8. **计划文件用完即删** — `ExitPlanMode` 或 `/init` 等操作生成的 plan 文件，执行完毕后及时清理，不提交入库

## Detailed References

- [01-repo-structure.md](.claude/instructions/01-repo-structure.md) — 完整目录结构与说明
- [02-note-conventions.md](.claude/instructions/02-note-conventions.md) — 笔记内容规范、wikilink、标题编号、代码块
- [03-git-workflow.md](.claude/instructions/03-git-workflow.md) — Git 工作流、commit 格式、squash 策略
- [04-shell-config.md](.claude/instructions/04-shell-config.md) — Shell 终端配置与编码处理
- [05-agent-coordination.md](.claude/instructions/05-agent-coordination.md) — 多 Agent 协作（Claude Code 为主）
- `~/.claude/CLAUDE.md` — 全局 CLAUDE.md
