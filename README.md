<p align="center">
  <img src="picture/cpplogo.png" alt="CPP Logo" width="120"/>
</p>

<h1 align="center">📚 C/C++ 系统编程知识库</h1>

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
  <a href="readme/README_EN.md"><img src="https://img.shields.io/badge/🌏-English-blue?style=for-the-badge" alt="English"/></a>
</p>

---

## 📖 项目简介

本仓库是一个 **个人学习笔记知识库**，围绕 C/C++ 系统编程、Linux 环境、计算机体系结构等主题持续积累。
所有笔记使用 **Markdown** 编写，通过 **Obsidian** 进行管理和同步。

> 🎯 **目标**：构建一份可检索、可复习的系统编程知识体系，覆盖从底层原理到工程实践的完整链路。

## ✨ 专题一览

| 🖥️ **C/C++** | 🐧 **Linux 环境** | ⚙️ **体系架构** |
|:---:|:---:|:---:|
| 语法基础 · 模板元编程 · 代码规范 · 项目结构 | Vim · g++/gdb · Makefile · 内核模块 | ARM32/64 · X86 汇编 · 内存模型 |

| 🛠️ **开发工具与构建** | 🌐 **网络编程** | 📱 **MCU 嵌入式** |
|:---:|:---:|:---:|
| CLion · VS2022 · CMake 入门/进阶 | Muduo 网络库 · IO 模型 | Boot-App 模式 · UART 内存注入 |

| 🗄️ **数据库** | 📝 **读书笔记** | 🎯 **更多专题** |
|:---:|:---:|:---:|
| SQL 语法 | C++ 最佳实践 · 开源项目分析 | GC 算法 · 调试优化(8篇) · 架构设计(5篇) · 并发与多线程 |

## 📂 目录结构

```
📦 obsidian_files
├── 📁 A-编程语言/              # C/C++/Go 语言基础
│   ├── 📁 01.C语言/           # C 基础 · 底层原理 · 系统编程
│   ├── 📁 02.C++/             # C++ 语法 · 规范 · 模板 · More Effective C++
│   └── 📁 03.Golang/          # Go 语言基础
├── 📁 B-构建与脚本/            # 构建工具与脚本语言
│   ├── 📁 01.构建工具/         # g++ · Makefile · CMake · 编译脚本
│   └── 📁 02.脚本语言/         # Shell · Lua · Python
├── 📁 C-Linux生态/             # Linux 全栈
│   ├── 📁 01.Linux环境/        # vim · 常用指令 · 动态库 · rpath · 加载与劫持
│   ├── 📁 02.Linux系统编程/     # 进程 · 内核 · 驱动
│   ├── 📁 03.Linux开发/        # RK3588 · Yocto · 交叉编译
│   ├── 📁 04.调试与优化/       # gdb · coredump · perf · 文件IO · 分支优化
│   ├── 📁 05.网络编程/         # Muduo · IO 模型
│   └── 📁 06.开源项目分析/     # Muduo/LevelDB/Redis/Nginx
├── 📁 D-系统与架构/            # 体系结构
│   ├── 📁 01.架构体系/         # ARM vs X86
│   ├── 📁 02.软件架构设计/     # PIMPL · CLI · 方法论 · 插件架构
│   ├── 📁 03.并发与内存/       # GC · atomic · 线程与异步
│   └── 📁 04.MCU嵌入式/        # MCU · ARM32 内存注入
├── 📁 E-杂项/                 # 工具与杂项
│   ├── 📁 01.开发工具/         # MobaXterm · CLion · VS2022 · Qt
│   ├── 📁 02.版本管理/         # Git · log 规范 · git bisect
│   ├── 📁 03.数据库/           # 🚧 施工中
│   ├── 📁 04.语言与标记/       # Markdown · XML · CSS · PlantUML · 英语
│   └── 📁 05.杂项/             # 🚧 暂空（内容已归入各模块）
├── 📁 picture/                  # 图片资源
├── 📁 readme/                   # 多语言 README
├── 📁 .claude/                  # Claude Code 配置
└── 📄 CLAUDE.md                 # AI 辅助配置
```

## 🚀 快速开始

```bash
# 克隆仓库
git clone git@github.com:xixishuibubao/obsidian_CPP.git

# 使用 Obsidian 打开 vault
# Obsidian → 打开其它仓库 → 选择本目录

# 同步更新
git pull origin main
```

## 📜 Git 工作流

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型       | 用途           |
|------------|----------------|
| `feat`     | 新增内容/功能   |
| `fix`      | 修复错误       |
| `docs`     | 文档类变更     |
| `style`    | 格式、命名规范  |
| `refactor` | 结构调整       |
| `chore`    | 工具配置       |

本地提交在推送前会合并整理，保持远端提交历史清晰。

## 📄 许可证

MIT © xixishuibubao77
