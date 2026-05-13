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
| `08.GUI与Qt/` | Qt framework notes |
| `09.读书笔记/` | Book notes (e.g., More Effective C++) |
| `10.辅助语言/` | Shell, Lua, Python, CMake; markup languages; PlantUML |
| `11.MCU嵌入式/` | Microcontroller development |
| `12.版本管理/` | Git usage and commit log conventions |
| `14.技术杂谈/` | Loading and hooking techniques |
| `15.内存管理/` | GC and memory management algorithms |
| `17.网络编程/` | Muduo network library, server projects |
| `20.模板操作/` | C++ templates |
| `22.调试与优化/` | Profiling with perf, performance tools |
| `24.开源学习/` | Open-source project analysis |
| `25.架构设计/` | PIMPL idiom, structured design, CLI design |
| `99.临时杂物间/` | Scratch/draft notes |

Directories `07`, `13`, `16`, `18`, `19`, `21`, `23` exist as placeholders (empty or containing only `.gitkeep`).

Images referenced by notes live in `/picture/`.

## Git & Obsidian Workflow

- **Primary sync method**: The [obsidian-git](https://github.com/Vinzent03/obsidian-git) plugin commits and pushes from within Obsidian.
- **Pre-commit hook**: A PowerShell script (`99.临时杂物间/auto-gitkeep.ps1` + `99.临时杂物间/pre-commit`) auto-creates/removes `.gitkeep` files so empty directories are tracked. The pre-commit hook calls this script before each commit.
- **Commit style**: See `12.版本管理/2. log规范.md` for conventions.
- **.gitignore**: Ignores `.obsidian/*` (with exceptions for plugin/themes config), large files, temp files, and editor artifacts.

## Note Conventions

- Written in **Chinese and English** — technical terms in English, explanations primarily in Chinese.
- Images embedded via `![description](picture/filename.png)`.
- Code snippets use standard markdown fenced blocks.
