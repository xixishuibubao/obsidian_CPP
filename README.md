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
  <img src="https://img.shields.io/badge/AI%20Agent-412991?style=flat-square&logo=openai&logoColor=white" alt="AI Agent"/>
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

| 🤖 **AI 辅助开发** | 📝 **读书笔记** | 🎯 **更多专题** |
|:---:|:---:|:---:|
| 编程范式演进 · Vibecoding · Workflow 选型 | C++ 最佳实践 · 开源项目分析 | GC 算法 · 调试优化(8篇) · 架构设计(5篇) · 并发与多线程 |

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
│   ├── 📁 01.Linux环境/        # vim · 常用指令 · 动态库 · rpath · 加载与劫持 · grep
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
├── 📁 E-AI与Agent协同开发/     # AI 辅助编程
│   ├── 📁 01.基础概念/         # 编程范式演进
│   ├── 📁 02.工作流与方法论/   # Vibecoding · AI 超级程序员路线 · 上下文管理 · 遗留代码分析 · 方法论选型 · Workflow 选型
│   ├── 📁 03.工具与配置/       # 🚧 占位
│   └── 📁 04.最佳实践/         # 🚧 占位
├── 📁 G-版本管理/              # Git 版本控制
│   ├── 1. git.md              # Git 完整教程
│   ├── 2. log规范.md          # Conventional Commits 规范
│   ├── 3. git bisect.md       # 二分查找定位 Bug
│   └── 4. 分支策略.md          # 分支模型对比
├── 📁 H-语言与标记/            # 标记语言与常用参考
│   ├── 1. Markdown.md         # Markdown 语法
│   ├── 2. CSS.md              # CSS 样式表
│   ├── 3. XML.md              # XML 基础
│   ├── 4. PlantUML学习资料.md  # PlantUML 学习路径
│   ├── 5. UML语法.md          # UML 类图语法
│   └── 6. 常用英语.md          # 编程英语词汇
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
