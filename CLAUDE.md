# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An **Obsidian vault** containing personal study notes on C/C++, systems programming, Linux, and related engineering topics. Organized as numbered markdown files by subject area.

This is **not a code project** — there are no build systems, no tests, and no compilable source. It is a knowledge base for reference and review.

## Repository Structure

Top-level directories are numbered by topic area:

| Directory | Topic |
|-----------|-------|
| `00.Golang/` | Go language basics |
| `01.C语法与技巧/` | C language and techniques |
| `02.C++语法与要点/` | C++ grammar, style, project structure |
| `03.Linux环境与工具/` | Vim, g++, gdb, makefile, shared/static libs |
| `04.架构体系/` | ARM vs x86 architecture |
| `05.Win工具/` | MobaXterm, CLion, VS2022 |
| `06.Linux开发/` | RK3588 board, Yocto builds |
| `07.数据库与SQL语法/` | Database and SQL (placeholder) |
| `08.GUI与Qt/` | Qt framework notes |
| `09.读书笔记/` | Book notes (e.g., More Effective C++) |
| `10.辅助语言/` | Shell, Lua, Python, CMake; markup languages; PlantUML |
| `11.MCU嵌入式/` | Microcontroller development |
| `12.版本管理/` | Git usage and commit log conventions |
| `13.通讯协议/` | Communication protocols (placeholder) |
| `14.技术杂谈/` | Loading and hooking techniques |
| `15.内存管理/` | GC and memory management algorithms |
| `16.数据结构与算法/` | Data structures and algorithms (placeholder) |
| `17.网络编程/` | Muduo network library, server projects |
| `18.并发与多线程/` | Concurrency and multithreading (placeholder) |
| `19.异常处理/` | Exception handling (placeholder) |
| `20.模板操作/` | C++ templates |
| `21.文件操作/` | File I/O operations (placeholder) |
| `22.调试与优化/` | Profiling with perf, performance tools |
| `23.测试框架/` | Testing frameworks (placeholder) |
| `24.开源学习/` | Open-source project analysis |
| `25.架构设计/` | PIMPL idiom, structured design, CLI design |
| `99.临时杂物间/` | Scratch/draft notes |

Images referenced by notes live in `/picture/`.

## Git & Obsidian Workflow

- **Primary sync method**: The [obsidian-git](https://github.com/Vinzent03/obsidian-git) plugin commits and pushes from within Obsidian. The plugin's `Custom Git binary path` setting must point to `git.exe` (not `git-bash.exe`).
- **Empty directories**: Tracked via `.gitkeep` files, managed manually (no pre-commit hook). Redundant `.gitkeep` files (in directories that now have content) should be removed with `git rm`.
- **Commit message format**: Must follow [Conventional Commits](https://www.conventionalcommits.org/) — use `type(scope): description` structure. Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`. See `12.版本管理/2. log规范.md` for full details.
- **Vault backup commits**: The obsidian-git plugin may create auto-backup commits with meaningless messages. These should be squashed/fixup'd into the preceding meaningful commit via `git rebase -i`.
- **.gitignore**: Ignores `.obsidian/*` (with exceptions for plugin/themes config), large files, temp files, and editor artifacts.

## Note Conventions

- Written in **Chinese and English** — technical terms in English, explanations primarily in Chinese.
- Images embedded via `![description](picture/filename.png)`.
- Code snippets use standard markdown fenced blocks.
- When cross-publishing to Feishu / WeChat Official Account, use [markdown.lovejade.cn](https://markdown.lovejade.cn/) for format conversion (select "公众号" mode).
- **File naming**: `数字. 空格 + 名称` (e.g., `1. C++基础.md`, `2. 代码规范.md`). Both directories and files follow this convention.
