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
| **图片引用** | `![描述](picture/文件名.png)` |
| **空目录占位** | 使用 `.gitkeep` 文件占位 |

## Common Workflows

### Create a New Note
1. **Place** in the appropriate subdirectory (e.g., `C-Linux生态/01.Linux环境/`)
2. **Name** as `N. Title.md` — N is the next available sort number within that subdirectory; internal title always starts at `# 1.`
3. **Content** follows sub-file [02-note-conventions.md](.claude/instructions/02-note-conventions.md): fenced code blocks + language annotation, wikilinks to related notes, bilingual (English terms + Chinese explanation)
4. **Images** go to `picture/` as `{section}-{seq}.png` (e.g., `3-1.png`); reference as `![desc](picture/file.png)` always lowercase `.png`
5. **Commit** with `docs(directory): what changed`

### Maintain Directories
- After creating/removing a directory, run the `.gitkeep` hook to sync empty-dir tracking:
  ```powershell
  powershell .git\hooks\auto-gitkeep.ps1
  ```
- Check repo state: `git status` / `git log --oneline -5`

### Useful Commands

```bash
# 近期变更概览
git log --oneline --name-status -10

# 查看某目录下有哪些笔记
ls -1 03.Linux环境与工具/

# 检查所有笔记标题是否以 "# 1." 开头（排除目录和配置文件）
grep -rn '^# \d' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'README' | grep -v '99\.'

# 统计各目录笔记数量
for d in [0-9]*/; do count=$(ls "$d"*.md 2>/dev/null | wc -l); [ "$count" -gt 0 ] && echo "$d → $count 篇"; done

# 查找无效的图片引用（标记引用但文件不存在）
grep -roP '\!\[.*?\]\(picture/[^)]+\)' . --include='*.md' | grep -v '\.git/'

# 查找可能断链的 wikilinks（未匹配文件名）
grep -roP '\[\[.+?\]\]' . --include='*.md' | grep -v '\.git/' | sort -u
```

## Directory Structure

```
A-编程语言/
├── 01.C语言/        ← C 基础 · 底层原理 · 系统编程
├── 02.C++/          ← C++ 语法 · 规范 · 模板
└── 03.Golang/       ← Go 语言基础

B-构建与脚本/
├── 01.构建工具/      ← g++ · Makefile · CMake · 编译脚本
└── 02.脚本语言/      ← Shell · Lua · Python

C-Linux生态/
├── 01.Linux环境/     ← vim · 常用指令 · tar · ssh · 库 · rpath
├── 02.Linux系统编程/  ← 进程 · CPU亲和 · 内核态/驱动/模块
├── 03.Linux开发/     ← RK3588 · Yocto · 交叉编译
├── 04.调试与优化/     ← gdb · coredump · perf · 文件IO · 分支优化
├── 05.网络编程/      ← Muduo · IO 模型
└── 06.开源项目分析/   ← Muduo · LevelDB · Redis · Nginx 等

D-系统与架构/
├── 01.架构体系/      ← ARM vs X86 汇编
├── 02.软件架构设计/   ← PIMPL · CLI · 结构化 · 方法论
├── 03.并发与内存/     ← GC · atomic · 线程与异步
└── 04.MCU嵌入式/     ← MCU 基础 · ARM32 内存注入

E-杂项/
├── 01.开发工具/      ← MobaXterm · CLion · VS2022 · Qt
├── 02.版本管理/      ← Git · log 规范
├── 03.数据库/        ← 🚧 占位
├── 04.语言与标记/     ← Markdown · CSS · XML · PlantUML · 英语
└── 05.杂项/          ← 读书笔记 · Hook/插件 · 临时杂物
```

## Key Rules

1. **每次改动后本地 commit，推远端前 squash** — 保持远端 log 清晰
2. **Commit 信息用 Conventional Commits 格式**
3. **笔记使用标准 Markdown**，无 YAML frontmatter，无 tags
4. **优先用 Git Bash**，乱码时回退 PowerShell
5. **目录变更后运行 `.gitkeep` hook**：`powershell .git\hooks\auto-gitkeep.ps1` — 自动创建/删除 `.gitkeep`
6. **CLAUDE.md 行数自管理**：根目录 CLAUDE.md 超过约 120 行时，将详细说明拆分至 `.claude/instructions/` 子文件，根文件始终保持全局指导的简洁性

## Detailed References

See `.claude/instructions/` for full documentation:

- [01-repo-structure.md](.claude/instructions/01-repo-structure.md) — 完整目录结构与说明
- [02-note-conventions.md](.claude/instructions/02-note-conventions.md) — 笔记内容规范、wikilink、标题编号、代码块
- [03-git-workflow.md](.claude/instructions/03-git-workflow.md) — Git 工作流、commit 格式、squash 策略
- [04-shell-config.md](.claude/instructions/04-shell-config.md) — Shell 终端配置与编码处理
