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
1. **Place** in the appropriate directory (e.g., `03.Linux环境与工具/`)
2. **Name** as `N. Title.md` — N is the next available sort number; internal title always starts at `# 1.`
3. **Content** follows sub-file [02-note-conventions.md](.claude/instructions/02-note-conventions.md): fenced code blocks + language annotation, wikilinks to related notes, bilingual (English terms + Chinese explanation)
4. **Images** go to `picture/` as `{section}-{seq}.png` (e.g., `3-1.png`); reference as `![desc](picture/file.png)` always lowercase `.png`
5. **Commit** with `docs(directory): what changed`

### Maintain Directories
- After creating/removing a directory, run the `.gitkeep` hook to sync empty-dir tracking:
  ```powershell
  powershell .git\hooks\auto-gitkeep.ps1
  ```
- Check repo state: `git status` / `git log --oneline -5`

## Directory Structure

| 目录 | 主题 | 目录 | 主题 |
|------|------|------|------|
| `00.Golang/` | Go 基础 | `11.MCU嵌入式/` | MCU + ARM32 注入 |
| `01.C语法与技巧/` | C 语言 | `12.版本管理/` | Git 操作 |
| `02.C++语法与要点/` | C++ 语法 | `14.技术杂谈/` | Hook 技术 |
| `03.Linux环境与工具/` | Vim/g++/gdb | `15.内存管理/` | GC 算法 |
| `04.架构体系/` | ARM vs X86 | `17.网络编程/` | Muduo |
| `05.Win工具/` | MobaXterm/CLion | `20.模板操作/` | C++ 模板 |
| `06.Linux开发/` | RK3588/Yocto | `22.调试与优化/` | Perf |
| `08.GUI与Qt/` | Qt | `24.开源学习/` | 项目分析 |
| `09.读书笔记/` | More Effective C++ | `25.架构设计/` | PIMPL/CLI |
| `10.辅助语言/` | 脚本/标记/建模语言 | `readme/` | 多语言 README |

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
