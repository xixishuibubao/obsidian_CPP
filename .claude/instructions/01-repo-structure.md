# 仓库结构说明

## 目录总览（A-H 语义分组）

仓库使用 `字母前缀-主题/序号.子主题/` 的语义分组结构，共八大模块：

### A-编程语言

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.C语言` | 3 | C 基础 · 底层原理 · 系统编程 |
| `02.C++` | 5 | C++ 基础 · 代码规范 · 项目结构 · 模板 · More Effective C++ |
| `03.Golang` | 1 | Go 语言基础 |

### B-构建与脚本

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.构建工具` | 5 | g++ · Makefile · CMake（入门/进阶）· 编译脚本设计 |
| `02.脚本语言` | 4 | Shell · Lua · Python（含 Telescope1126 常用语法速查）· **C/C++ 与 Python 互调用** |

### C-Linux生态（最大模块，6个子目录）

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.Linux环境` | **6** | vim/常用指令 · 动态库与静态库 · rpath · 加载与劫持 · grep 文本搜索 · **Linux 目录结构** |
| `02.Linux系统编程` | **7** | 进程管理 · CPU亲和性 · 用户态/内核态 · 字符设备驱动 · 内核模块开发 · 进程间通信 · **dup 函数** |
| `03.Linux开发` | **5** | RK3588 · Yocto · 交叉编译优化选项 · 容器化与系统构建 · **Buildroot** |
| `04.调试与优化` | **9**（最大子目录） | gdb · coredump · perf · 文件IO · 分支优化 · 综合调试 · **Valgrind 内存调试** |
| `05.网络编程` | 2 | Muduo 网络库 · IO 模型 |
| `06.开源项目分析` | 2 | 按类别编排的源码分析合集 · 服务器开源项目 |
| `07.Telescope1126实战` | **11** | 1126B 工作项目：总览 · 双进程 · IPC · pybind · V4L2 · 交叉编译 · adb · Tornado · FITS · MPP · OTA |

### D-系统与架构

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.架构体系` | 1 | ARM vs X86 汇编 |
| `02.软件架构设计` | **5** | PIMPL · 结构化设计 · CLI 设计 · Claude Code Skill 方法论 · 插件架构设计 |
| `03.并发与内存` | 3 | GC 算法 · atomic 与内存序 · 线程与异步 |
| `04.MCU嵌入式` | 2 | MCU 开发基础 · ARM32 内存注入（UART） |

### E-AI与Agent协同开发

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.基础概念` | 1 | 编程范式演进（Spec Coding → Agentic → Harness） |
| `02.工作流与方法论` | **6** | Vibecoding 最佳实践 · AI 辅助超级程序员工作流 · Claude Code 上下文管理 · 遗留代码系统分析 · 方法论选型 · **Skill 工程化与 Workflow 选型** |
| `03.工具与配置` | 0 | 🚧 占位（MCP · CLI skills · AGENT.md） |
| `04.最佳实践` | 0 | 🚧 占位（案例研究 · 经验总结） |

### G-版本管理

| 笔记 | 内容 |
|------|------|
| `1. git.md` | Git 完整教程：仓库配置 · 分支 · 合并 · rebase · 暂存 · 重置 |
| `2. log规范.md` | Conventional Commits 规范（类型 · scope · BREAKING CHANGE · SemVer） |
| `3. git bisect.md` | 二分查找定位 Bug 提交（手动 + 自动 run） |
| `4. 分支策略.md` | Git Flow · GitHub Flow · GitLab Flow · Trunk-Based 对比 |

### H-语言与标记

| 笔记 | 内容 |
|------|------|
| `1. Markdown.md` | Markdown 语法参考（标题 · 列表 · 代码 · 链接 · 表格） |
| `2. CSS.md` | CSS 样式表（🚧 待补充） |
| `3. XML.md` | XML 基础语法示例 |
| `4. PlantUML学习资料.md` | PlantUML 学习路径（书籍 · 文档 · 实操建议） |
| `5. UML语法.md` | PlantUML 类图语法 + SOLID 设计原则 |
| `6. 常用英语.md` | 编程常用英语词汇表（~72 词条） |

### 其他顶层目录

| 目录 | 内容 |
|------|------|
| `picture/` | 图片资源，命名格式 `{章节号}-{序号}.png`（如 `5-1-1.png`） |
| `readme/` | 多语言 README 文件 |
| `.claude/` | Claude Code 辅助配置与指令文件（含 `agents/` 代理定义、`instructions/` 子指令） |

## 总体统计

- **总笔记数**：~87 篇
- **最大模块**：C-Linux生态（**41** 篇笔记）
- **最大子目录**：C-Linux生态/04.调试与优化（8 篇）
- **空子目录**：E-AI与Agent协同开发/03.工具与配置, E-AI与Agent协同开发/04.最佳实践

## 图片资源

位于 `/picture/`，命名格式为 `{章节号}-{序号}.png`。全部使用小写 `.png` 扩展名。

当前图片列表：
- `cpplogo.png` — 项目 Logo
- `linux_server.png` — 网络编程章节

## 特殊文件

- `CLAUDE.md` — 项目级 Claude Code 指引（本文件的上层入口）
- `README.md` — 项目介绍（中文，默认显示）
- `readme/README_EN.md` — 项目介绍（英文版）
- `.gitignore` — 忽略 `.obsidian/*`（白名单插件/主题）、大文件、编辑器临时文件
