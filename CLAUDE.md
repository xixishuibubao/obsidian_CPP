# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An **Obsidian vault** containing personal study notes on C/C++, systems programming, Linux, and related engineering topics. Organized as numbered markdown files by subject area.

This is **not a code project** — there are no build systems, no tests, and no compilable source. It is a knowledge base for reference and review.

Images referenced by notes live in `/picture/`.

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
4. **Images** go to `picture/` as `{section}-{seq}.png` (e.g., `3-1.png`); reference as `![desc](picture/file.png)`
5. **Commit** with `docs(directory): what changed`

### Maintain Directories
- After creating/removing a directory, run the `.gitkeep` hook:
  ```powershell
  powershell .git\hooks\auto-gitkeep.ps1
  ```
- Check repo state: `git status` / `git log --oneline -5`

### Sync via Obsidian-Git (日常同步)
Vault 通过 [obsidian-git](https://github.com/Vinzent03/obsidian-git) 插件同步。`Custom Git binary path` 必须指向 `git.exe`。

```bash
# 标准同步
git pull --rebase origin main

# 处理冲突
git diff --name-only --diff-filter=U       # 查看冲突文件
# 编辑后：
git add <冲突文件> && git commit -m "fix(vault): resolve merge conflict"

# 紧急回退
git reflog && git reset --hard HEAD@{N}
```

> ⚠️ Pull 前确保所有本地变更已 commit。如有未 commit 修改导致 pull 失败，先 `git stash` 暂存。

### Squash Before Push

推远端前整理本地 commits：

```bash
# 方案一：交互式 rebase（推荐，控制力强）
git rebase -i HEAD~N

# 方案二：soft reset（仅保留一版）
git reset --soft HEAD~N && git commit -m "type(scope): description"
```

详细 squash 策略参见 [03-git-workflow.md](.claude/instructions/03-git-workflow.md)。

## Useful Commands

Commands grouped by task. All paths relative to vault root.

### 📋 统计
```bash
# 近期变更
git log --oneline --name-status -10

# 各目录笔记数量
for d in A-*/ B-*/ C-*/ D-*/ E-*/; do count=$(ls "$d"*.md 2>/dev/null | wc -l); [ "$count" -gt 0 ] && echo "${d%/} → $count 篇"; done

# 查看某目录笔记列表
ls -1 C-Linux生态/01.Linux环境/
```

### ✅ 完整性检查
```bash
# 标题格式（检查非 1 级标题）
grep -rn '^# \d' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'README' | grep -v '99\.'

# 可能断裂的 wikilinks（排除 shell [[ 条件中的 $ 变量）
grep -roP '\[\[[^$\][]+?\]\]' . --include='*.md' | grep -v '\.git/' | sort -u

# 引用不存在图片的链接
grep -roP '\!\[.*?\]\(picture/[^)]+\)' . --include='*.md' | grep -v '\.git/'
```

### 🔧 维护
```bash
# 批量修复 LF → CRLF（Windows 兼容）
git add --renormalize .

# 运行 .gitkeep hook
powershell .git\hooks\auto-gitkeep.ps1
```

## Directory Overview

```
A-编程语言/          ← C · C++ · Golang
B-构建与脚本/        ← g++ · Makefile · CMake · Shell · Lua · Python
C-Linux生态/         ← Linux 环境 · 系统编程 · 开发 · 调试优化 · 网络 · 开源分析
D-系统与架构/        ← 汇编 · 架构设计 · 并发/内存 · MCU
E-杂项/             ← 开发工具 · Git · 语言/标记 · （数据库 🚧 占位）
```

Detailed directory structure with note counts and descriptions: [01-repo-structure.md](.claude/instructions/01-repo-structure.md)

## Key Rules

1. **每次改动后本地 commit，推远端前 squash** — 保持远端 log 清晰
2. **Commit 用 Conventional Commits 格式**：`type(scope): description`，内容优先用简体中文
3. **笔记使用标准 Markdown**，无 YAML frontmatter，无 tags
4. **终端优先用 Bash**，中文乱码时回退 PowerShell
5. **目录变更后运行 `.gitkeep` hook**：`powershell .git\hooks\auto-gitkeep.ps1`
6. **本文件保持简洁**（~150 行上限），详细规则拆分至 `.claude/instructions/` 子文件

## Detailed References

- [01-repo-structure.md](.claude/instructions/01-repo-structure.md) — 完整目录结构与说明
- [02-note-conventions.md](.claude/instructions/02-note-conventions.md) — 笔记内容规范、wikilink、标题编号、代码块
- [03-git-workflow.md](.claude/instructions/03-git-workflow.md) — Git 工作流、commit 格式、squash 策略
- [04-shell-config.md](.claude/instructions/04-shell-config.md) — Shell 终端配置与编码处理
