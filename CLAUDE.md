# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An **Obsidian vault** containing personal study notes on C/C++, systems programming, Linux, and related engineering topics. Organized as numbered markdown files by subject area.

This is **not a code project** — there are no build systems, no tests, and no compilable source. It is a knowledge base for reference and review.

Images referenced by notes live in `/picture/`. English readers see [README_EN.md](readme/README_EN.md).

## Quick Reference

| 项目 | 规则 |
|------|------|
| **笔记引用** | Obsidian wikilink `[[文件名\|显示文字]]` |
| **标题格式** | `# 1.`, `## 1.1`, `### 1.1.1` 数字编号 |
| **Frontmatter** | 不使用 YAML frontmatter 或 tags |
| **图片引用** | `![描述](picture/文件名.png)`，后缀统一 `.png` |
| **编码** | 中文内容优先 Bash，乱码时回退 PowerShell 并设 `LC_ALL=C.UTF-8` |
| **空目录占位** | 使用 `.gitkeep` 文件占位 |

## Common Workflows

### Create a New Note
1. **Place** in the appropriate subdirectory (e.g., `C-Linux生态/01.Linux环境/`)
2. **Name** as `N. Title.md` — N is the next available sort number within that subdirectory; internal title always starts at `# 1.`
3. **Content** follows [02-note-conventions.md](.claude/instructions/02-note-conventions.md): fenced code blocks + language annotation, wikilinks to related notes, bilingual (English terms + Chinese explanation)
4. **Images** go to `picture/` as `{section}-{subsection}-{seq}.png` (e.g., `5-1-1.png`); reference as `![desc](picture/file.png)`
5. **Commit** with `docs(目录): 新增了什么内容`（description 用简体中文）

### Rename / Move a Note
1. Update the file name and `# 1.` title header inside it
2. Update all `[[old-name]]` wikilinks across the vault:
   ```bash
   grep -roP '\[\[old-name(?:\|.*?)?\]\]' . --include='*.md' | grep -v '\.git/'
   ```
3. Fix image paths in the moved note if the section number changed
4. Commit with `refactor(目录): 描述`

### Maintain Directories
- After creating/removing a directory, run the `.gitkeep` hook:
  ```powershell
  powershell -File .git\hooks\auto-gitkeep.ps1
  ```
  > 脚本不存在时，手动补齐：`Get-ChildItem -Directory -Recurse | Where-Object { (Get-ChildItem $_.FullName -File -Exclude '.gitkeep').Count -eq 0 } | ForEach-Object { New-Item -ItemType File -Path (Join-Path $_.FullName '.gitkeep') -Force }`
- Check repo state: `git status` / `git log --oneline -5`

### Sync via Obsidian-Git
Vault 通过 [obsidian-git](https://github.com/Vinzent03/obsidian-git) 插件同步。`Custom Git binary path` 必须指向 `git.exe`。

```bash
git pull --rebase origin main                    # 标准同步
git diff --name-only --diff-filter=U             # 查看冲突文件
git add <文件> && git commit -m "fix(vault): 描述" # 解决冲突
git reflog && git reset --hard HEAD@{N}          # 紧急回退
```

> ⚠️ Pull 前确保所有本地变更已 commit。obsidian-git 可能产生自动备份提交，squash 时标记为 `fixup`。

### Squash Before Push
```bash
# 交互式 rebase（推荐）
git rebase -i HEAD~N

# 或 soft reset（仅保留一版）
git reset --soft HEAD~N && git commit -m "type(scope): description"
```

详见 [03-git-workflow.md](.claude/instructions/03-git-workflow.md)。

## Useful Commands

All paths relative to vault root.

### 📋 统计
```bash
# 近期变更
git log --oneline --name-status -10

# 各模块笔记数（Bash）
for d in A-*/ B-*/ C-*/ D-*/ E-*/; do count=$(ls "$d"*.md 2>/dev/null | wc -l); [ "$count" -gt 0 ] && echo "${d%/} → $count 篇"; done

# 各模块笔记数（PowerShell）
@("A-编程语言","B-构建与脚本","C-Linux生态","D-系统与架构","E-杂项") | % { $c = (Get-ChildItem "$_\*.md" -Recurse -File | Measure-Object).Count; "$_ → $c 篇" }
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

```
A-编程语言/          ← C · C++ · Golang
B-构建与脚本/        ← g++ · Makefile · CMake · Shell · Lua · Python
C-Linux生态/         ← Linux 环境 · 系统编程 · 开发 · 调试优化 · 网络 · 开源分析
D-系统与架构/        ← 汇编 · 架构设计 · 并发/内存 · MCU
E-杂项/             ← 开发工具 · Git · 语言/标记 · （数据库 🚧 占位）
```

~69 篇笔记，完整结构与计数见 [01-repo-structure.md](.claude/instructions/01-repo-structure.md)。

## Key Rules

1. **每次改动后本地 commit，推远端前 squash** — 保持远端 log 清晰
2. **Commit 用 Conventional Commits 格式**：`type(scope): description`，内容优先用简体中文
3. **笔记使用标准 Markdown**，无 YAML frontmatter，无 tags
4. **终端优先用 Bash**，中文乱码时回退 PowerShell
5. **目录变更后运行 `.gitkeep` hook**
6. **本文件保持简洁**（~150 行上限），详细规则拆分至 `.claude/instructions/` 子文件

## Claude Code Skills

可用 slash commands（在 vault 根目录调用）:

| Command | 用途 |
|---------|------|
| `/quick-commit` | 自动 stage → 分析 diff → 生成 Conventional Commit → 确认后执行 |
| `/squash-commits` | 推送前整理本地 commits，自动检测 obsidian-git 备份提交 |
| `/init-note-vault` | 初始化笔记规范（支持默认/精简模式） |
| `/init-win-env` | 探测本机 Git Bash/PowerShell，生成终端规则与权限预设 |
| `/fewer-permission-prompts` | 扫描 transcripts 自动生成权限白名单 |

## .gitignore 策略

```
.obsidian/*                        # 忽略所有 Obsidian 配置
!.obsidian/community-plugins.json  # 但保留插件列表
!.obsidian/core-plugins.json       # 和核心插件配置
!.obsidian/plugins/obsidian-git/*  # 和 Git 插件配置
!.obsidian/themes/**/*             # 和主题配置
```

大文件（`.mp4`, `.pdf`, `.zip`）和编辑器临时文件同样被忽略。

## Detailed References

- [01-repo-structure.md](.claude/instructions/01-repo-structure.md) — 完整目录结构与说明
- [02-note-conventions.md](.claude/instructions/02-note-conventions.md) — 笔记内容规范、wikilink、标题编号、代码块
- [03-git-workflow.md](.claude/instructions/03-git-workflow.md) — Git 工作流、commit 格式、squash 策略
- [04-shell-config.md](.claude/instructions/04-shell-config.md) — Shell 终端配置与编码处理
- [`~/.claude/CLAUDE.md`](file:///C:/Users/AS/.claude/CLAUDE.md) — 全局 CLAUDE.md
