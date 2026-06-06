<p align="center">
  <img src="../picture/cpplogo.png" alt="CPP Logo" width="120"/>
</p>

<h1 align="center">📚 C/C++ Systems Programming Knowledge Base</h1>

<p align="center">
  <img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=white" alt="C"/>
  <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++"/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux"/>
  <img src="https://img.shields.io/badge/ARM-0091BD?style=flat-square&logo=arm&logoColor=white" alt="ARM"/>
  <img src="https://img.shields.io/badge/CMake-064F8C?style=flat-square&logo=cmake&logoColor=white" alt="CMake"/>
  <img src="https://img.shields.io/badge/Obsidian-7C3AED?style=flat-square&logo=obsidian&logoColor=white" alt="Obsidian"/>
  <img src="https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white" alt="Markdown"/>
</p>

<p align="center">
  <a href="../README.md"><img src="https://img.shields.io/badge/🌏-中文-red?style=for-the-badge" alt="中文"/></a>
</p>

---

## 📖 About

This is a **personal study notes knowledge base** focused on C/C++ systems programming, Linux environment, computer architecture, and related engineering topics. All notes are written in **Markdown** and managed via **Obsidian**.

> 🎯 **Goal**: Build a searchable, reviewable systems programming knowledge system covering the full spectrum from low-level principles to engineering practices.

## ✨ Topics

| 🖥️ **C/C++** | 🐧 **Linux Env** | ⚙️ **Architecture** |
|:---:|:---:|:---:|
| Grammar · Templates · Coding Standards · Project Structure | Vim · g++/gdb · Makefile · Shared/Static Libs | ARM32/64 · X86 ASM · Memory Model |

| 🛠️ **Dev Tools** | 🌐 **Networking** | 📱 **Embedded MCU** |
|:---:|:---:|:---:|
| CLion · VS2022 · MobaXterm · CMake | Muduo Library · Server Projects | Boot-App Mode · UART Communication |

| 🗄️ **Database** | 📝 **Book Notes** | 🎯 **More Topics** |
|:---:|:---:|:---:|
| SQL Grammar | More Effective C++ · Open Source Analysis | GC Algorithms · Profiling · Architecture Design |

## 📂 Directory Layout

```
📦 obsidian_files
├── 📁 00.Golang/               # Go basics
├── 📁 01.C语法与技巧/           # C language · low-level · system programming
├── 📁 02.C++语法与要点/         # C++ basics · code standards · project structure
├── 📁 03.Linux环境与工具/       # Vim · g++ · gdb · Makefile · commands
├── 📁 04.架构体系/              # ARM vs X86 · ASM fundamentals
├── 📁 05.Win工具/               # MobaXterm · CLion · VS2022
├── 📁 06.Linux开发/             # RK3588 · Yocto builds
├── 📁 08.GUI与Qt/               # Qt framework
├── 📁 09.读书笔记/              # More Effective C++ etc.
├── 📁 10.辅助语言/              # Scripting/markup/modeling languages + English vocab
├── 📁 11.MCU嵌入式/             # MCU development · ARM32 memory injection
├── 📁 12.版本管理/              # Git guide · commit conventions
├── 📁 14.技术杂谈/              # Loading & hooking techniques
├── 📁 15.内存管理/              # GC algorithms
├── 📁 17.网络编程/              # Muduo · IO models · Socket programming
├── 📁 20.模板操作/              # C++ template metaprogramming
├── 📁 22.调试与优化/            # Perf analysis · performance tools
├── 📁 24.开源学习/              # Open-source project analysis
├── 📁 25.架构设计/              # PIMPL · CLI design
├── 📁 99.临时杂物间/            # Scratch notes
├── 📁 picture/                  # Image assets
├── 📁 readme/                   # Multi-language README
├── 📁 .claude/                  # Claude Code config
└── 📄 CLAUDE.md                 # AI assistant config
```

## 🚀 Getting Started

```bash
# Clone the repo
git clone git@github.com:xixishuibubao/obsidian_CPP.git

# Open as Obsidian vault
# Obsidian → Open another vault → Select this directory

# Pull latest changes
git pull origin main
```

## 📜 Git Workflow

This repository follows [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

| Type       | Usage                  |
|------------|------------------------|
| `feat`     | New content / feature  |
| `fix`      | Bug / error fix        |
| `docs`     | Documentation          |
| `style`    | Formatting, naming     |
| `refactor` | Restructuring          |
| `chore`    | Tooling, config        |

Local commits are squashed before pushing to remote to maintain a clean history.

## 📄 License

MIT © xixishuibubao77
