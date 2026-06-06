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
| 语法基础 · 模板元编程 · 代码规范 · 项目结构 | Vim · g++/gdb · Makefile · 动态/静态库 | ARM32/64 · X86 汇编 · 内存模型 |

| 🛠️ **开发工具** | 🌐 **网络编程** | 📱 **MCU 嵌入式** |
|:---:|:---:|:---:|
| CLion · VS2022 · MobaXterm · CMake | Muduo 网络库 · 服务器项目 | Boot-App 模式 · UART 通讯 |

| 🗄️ **数据库** | 📝 **读书笔记** | 🎯 **更多专题** |
|:---:|:---:|:---:|
| SQL 语法 | More Effective C++ · 开源项目分析 | GC 算法 · 调试优化 · 架构设计 |

## 📂 目录结构

```
📦 obsidian_files
├── 📁 00.Golang/               # Go 语言基础
├── 📁 01.C语法与技巧/           # C 语言常用 · 底层原理 · 系统编程
├── 📁 02.C++语法与要点/         # C++ 基础 · 代码规范 · 项目结构
├── 📁 03.Linux环境与工具/       # Vim · g++ · gdb · Makefile · 常用指令
├── 📁 04.架构体系/              # ARM vs X86 架构 · 汇编基础
├── 📁 05.Win工具/               # MobaXterm · CLion · VS2022
├── 📁 06.Linux开发/             # RK3588 · Yocto 构建
├── 📁 07.数据库与SQL语法/       # 🚧 施工中
├── 📁 08.GUI与Qt/               # Qt 框架笔记
├── 📁 09.读书笔记/              # More Effective C++ 等
├── 📁 10.辅助语言/              # 脚本/标记/建模语言 + 英语词汇
├── 📁 11.MCU嵌入式/             # MCU 开发 · ARM32 内存注入
├── 📁 12.版本管理/              # Git 操作指南 · 提交规范
├── 📁 14.技术杂谈/              # 加载与劫持技术
├── 📁 15.内存管理/              # GC 回收算法
├── 📁 17.网络编程/              # Muduo · IO 模型 · Socket 编程
├── 📁 20.模板操作/              # C++ 模板元编程
├── 📁 22.调试与优化/            # Perf 分析 · 性能工具
├── 📁 24.开源学习/              # 开源项目分析
├── 📁 25.架构设计/              # PIMPL · CLI 设计
├── 📁 99.临时杂物间/            # 草稿笔记
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
