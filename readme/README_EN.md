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
  <img src="https://img.shields.io/badge/AI%20Agent-412991?style=flat-square&logo=openai&logoColor=white" alt="AI Agent"/>
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
| Grammar · Standards · Templates · More Effective C++ | Commands · g++/gdb · Makefile · Kernel | ARM32/64 · X86 · Memory Model |

| 🛠️ **Dev Tools & Build** | 🌐 **Networking** | 📱 **Embedded MCU** |
|:---:|:---:|:---:|
| CLion · VS2022 · CMake (Beginner→Advanced) | Muduo Library · IO Models | Boot-App Mode · UART Memory Injection |

| 🤖 **AI-Assisted Dev** | 📝 **Book Notes** | 🎯 **More Topics** |
|:---:|:---:|:---:|
| Paradigm Evolution · Vibecoding · Workflows | C++ Best Practices · Open Source | GC · Profiling (10) · Architecture (5) · Linux Dev (5) |

## 📂 Directory Layout

```plain
📦 obsidian_files
├── 📁 A-编程语言/              # Languages
│   ├── 📁 01.C语言/           # C · low-level · system programming
│   ├── 📁 02.C++/             # C++ syntax · standards · templates · More Effective C++
│   └── 📁 03.Golang/          # Go basics
├── 📁 B-构建与脚本/            # Build & scripting
│   ├── 📁 01.构建工具/         # g++ · Makefile · CMake · build scripts · linker scripts
│   └── 📁 02.脚本语言/         # Shell · Lua · Python · C/C++↔Python
├── 📁 C-Linux生态/             # Linux ecosystem
│   ├── 📁 01.Linux环境/        # commands · dynamic libs · rpath · dlopen · grep
│   ├── 📁 02.Linux系统编程/     # processes · kernel · drivers · IPC
│   ├── 📁 03.Linux开发/        # RK3588 · cross-compilation · build systems · Buildroot · Rockchip partitions
│   ├── 📁 04.调试与优化/       # gdb · perf · Valgrind · etc. (10 notes)
│   ├── 📁 05.网络编程/         # Muduo · IO models
│   └── 📁 06.开源项目分析/     # open source · servers · mjpg-streamer
├── 📁 D-系统与架构/            # Systems & architecture
│   ├── 📁 01.架构体系/         # ARM vs X86
│   ├── 📁 02.软件架构设计/     # PIMPL · CLI · methodology · plugin architecture
│   ├── 📁 03.并发与内存/       # GC · atomic · threads & async
│   └── 📁 04.MCU嵌入式/        # MCU · ARM32 memory injection
├── 📁 E-AI与Agent协同开发/     # AI-assisted development
│   ├── 📁 01.基础概念/         # Paradigm evolution
│   ├── 📁 02.工作流与方法论/   # Vibecoding · Super Programmer roadmap · context management · legacy code analysis
│   ├── 📁 03.工具与配置/       # tools & MCP index
│   └── 📁 04.最佳实践/         # best practices index
├── 📁 F-版本管理/              # Version control
│   ├── 1. git.md              # Git complete tutorial
│   ├── 2. log规范.md          # Conventional Commits
│   ├── 3. git bisect.md       # Git bisect bug hunting
│   └── 4. 分支策略.md          # Branching strategies
├── 📁 G-语言与标记/            # Languages & markup
│   ├── 1. Markdown.md         # Markdown syntax
│   ├── 2. CSS.md              # CSS styles
│   ├── 3. XML.md              # XML basics
│   ├── 4. PlantUML学习资料.md  # PlantUML resources
│   ├── 5. UML语法.md          # UML class diagram syntax
│   ├── 6. 常用英语.md          # Programming English vocab
│   ├── 7. INI语法.md          # INI config syntax
│   └── 8. YAML语法.md         # YAML config syntax
├── 📁 picture/
├── 📁 readme/
├── 📁 .claude/
└── 📄 CLAUDE.md
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
