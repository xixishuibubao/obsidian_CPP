# 仓库结构说明

## 目录总览（A–G 语义分组）

仓库使用 `字母前缀-主题/序号.子主题/` 的语义分组结构，共七大模块（A–G，无 H- 前缀）：

### A-编程语言

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.C语言` | 3 | C 基础 · 底层原理 · 系统编程 |
| `02.C++` | 4 | C++ 基础 · 代码规范 · 模板 · More Effective C++ |
| `03.Golang` | 1 | Go 语言基础 |

### B-构建与脚本

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.构建工具` | 7 | g++ · Makefile · CMake（入门/进阶）· 编译脚本设计 · 分布式编译 · **链接脚本** |
| `02.脚本语言` | 4 | Shell · Lua · Python · **C/C++ 与 Python 互调用** |

### C-Linux生态（最大模块，6 个子目录）

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.Linux环境` | **8** | 常用指令 · 动态库与静态库 · rpath · 加载与劫持 · grep · Linux 目录结构 · 启动流程 · NFS |
| `02.Linux系统编程` | **8** | 进程管理 · CPU 亲和性 · 用户态/内核态 · 字符设备驱动 · 内核模块 · IPC · dup · popen/system |
| `03.Linux开发` | **5** | RK3588 · 交叉编译优化 · 容器化与系统构建 · Buildroot · **Rockchip 分区** |
| `04.调试与优化` | **10**（最大子目录） | gdb · coredump · 基本调优 · perf · 高性能工具 · 文件 IO · 分支优化 · 综合调试 · Valgrind · CPU 高占用 |
| `05.网络编程` | 2 | Muduo · IO 模型 |
| `06.开源项目分析` | **3** | 开源项目分析合集 · 服务器项目 · **mjpg-streamer** |

### D-系统与架构

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.架构体系` | 2 | ARM vs X86 · 跨平台动态库加载机制 |
| `02.软件架构设计` | 5 | PIMPL · 结构化设计 · CLI 设计 · Skill 方法论 · 插件架构 |
| `03.并发与内存` | 3 | GC · atomic 与内存序 · 线程与异步 |
| `04.MCU嵌入式` | 2 | MCU 开发基础 · ARM32 内存注入（UART） |

### E-AI与Agent协同开发

| 子目录 | 笔记数 | 内容 |
|--------|--------|------|
| `01.基础概念` | 1 | 编程范式演进 |
| `02.工作流与方法论` | 6 | Vibecoding · 超级程序员 · 上下文管理 · 遗留代码分析 · 方法论选型 · Skill/Workflow |
| `03.工具与配置` | **5** | 工具与配置索引 · /agent 使用指南 · Team 模式协作 · 模式对比与选型 · **Skill 总览与推荐清单** |
| `04.最佳实践` | 1 | 最佳实践索引（占位扩展） |

### F-版本管理

| 笔记 | 内容 |
|------|------|
| `1. git.md` | Git 完整教程 |
| `2. log规范.md` | Conventional Commits |
| `3. git bisect.md` | 二分定位 Bug |
| `4. 分支策略.md` | 分支模型对比 |

### G-语言与标记

| 笔记 | 内容 |
|------|------|
| `1. Markdown.md` | Markdown 语法 |
| `2. CSS.md` | CSS 基础与常用场景 |
| `3. XML.md` | XML 基础语法 |
| `4. PlantUML学习资料.md` | PlantUML 学习路径 |
| `5. UML语法.md` | UML 类图 · SOLID |
| `6. 常用英语.md` | 编程英语词汇 |
| `7. INI语法.md` | INI 配置 |
| `8. YAML语法.md` | YAML 配置 |

### 其他顶层

| 路径 | 内容 |
|------|------|
| `picture/` | 图片资源（`cpplogo.png`、`linux_server.png`） |
| `readme/` | 多语言 README |
| `.claude/` | Claude Code 指令与配置（含 `instructions/`、`skills/`、`plan/`） |
| `.claude/plan/` | Plan 模式产出的计划与思考快照（`.plan.md`） |
| `.claude/skills/` | 7 个可复用 Skill（见下表） |

**`.claude/skills/` 子目录**：

| Skill | 定位 | 类型 |
|-------|------|------|
| `ingest-note` | 知识入库：清洗→落盘→索引 | 日常 |
| `quick-commit` | 分析 diff→Conventional Commit | 日常 |
| `squash-commits` | 推送前 squash、清理备份提交 | 日常 |
| `vault-audit` | 全库/增量机械审计 + 分模块语义审查 | 日常 |
| `init-win-env` | Windows Shell/Git 环境探测 | 一次性 |
| `init-git-convention` | Git 工作流规范注入 | 一次性 |
| `init-note-vault` | 笔记格式规范初始化 | 一次性 |

索引详见 [`.claude/skills/README.md`](../skills/README.md)。
| `.cursor/rules/` | Cursor 规则（对齐 Claude Code） |

## 总体统计

- **总笔记数**：88 篇（截至 2026-07，7 大模块 A–G）
- **最大模块**：C-Linux生态（**36** 篇）
- **最大子目录**：C-Linux生态/04.调试与优化（**10** 篇）

## 图片资源

位于 `/picture/`，全部小写 `.png`：

- `cpplogo.png` — 项目 Logo（README）
- `linux_server.png` — 网络编程章节

## 特殊文件

- `CLAUDE.md` — 项目级 Claude Code 指引
- `.claude/instructions/05-agent-coordination.md` — 多 Agent 协作
- `.claude/instructions/07-plan-mode.md` — Plan 模式计划文件
- `README.md` / `readme/README_EN.md` — 项目介绍
