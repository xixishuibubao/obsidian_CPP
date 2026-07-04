---
name: ingest-note
description: 将零散原始文本清洗为本 vault 风格 Markdown，A–G 分类落盘、补 wikilink、更新索引。Use when 整理/入库笔记、/ingest-note、处理 raw 文件
---

# /ingest-note — 笔记摄入与格式化

将零散的原始知识文本清洗为本项目风格的 Markdown 笔记，自动定位到合适的目录，更新索引和 README，删除源文件；**仅当用户明确要求时**生成规范 commit。

---

## 核心工作流

### 1. 输入接收

- 如果对话中包含文件路径参数（如 `/ingest-note ./raw/foo.md`），读取该文件
- 否则从用户消息中提取粘贴的原始文本内容
- 若用户仅口述主题与要点，先起草笔记骨架，请用户补充后再继续
- 存入变量 `raw_content`

> 不要混淆：多个文件传入时逐个处理，但作为一次 `ingest` 会话整体提交。

**用户侧可加速归类**（可选提供）：主题/领域、原始材料、目标笔记偏好（新建 vs 并入某篇）、深度（仅提纲 / 仅详情 / 双分区都要）。

### 2. 内容分析与结构拆解

先用 `Read` 读取 `README.md`、`.claude/instructions/01-repo-structure.md`、`.claude/instructions/02-note-conventions.md` 和受影响目录的笔记列表，建立对知识库结构的完整理解。

然后分析 `raw_content`，按以下维度拆解：

| 维度 | 说明 |
|------|------|
| **逻辑块边界** | 按标题层级（`#`/`##`）、分隔线 `---`、或明显主题切换拆分 |
| **主题领域** | 匹配 A–G 七大模块（见下表） |
| **目标目录** | 从已有目录结构和笔记主题推断最匹配的子目录 |
| **操作类型** | 新建文件 / 扩展现有文件（追加到末尾或插入合适位置） |

**模块对照**：见 [01-repo-structure.md](../../instructions/01-repo-structure.md) 目录总览（A–G 七大模块）。

对每个逻辑块，标注其核心内容摘要、目标路径和操作方式。

### 3. 格式化（项目规范适配）

将每个逻辑块按照 [02-note-conventions.md](../../instructions/02-note-conventions.md) 格式化：

```
# N. 标题                     ← 内部标题从 # 1. 起始
## N.M 二级标题
```

| 规范 | 规则 |
|------|------|
| **标题编号** | `# N.` / `## N.M` / `### N.M.O`，文件内从 `# 1.` 开始 |
| **文件命名** | 扫描目标目录，取最大序号 +1，格式 `N. 标题.md` |
| **代码块** | fenced + 小写语言标注（`c` / `cpp` / `bash` / `powershell` / `makefile` / `go` / `python` / `lua` / `java` / `sql` / `plain`） |
| **双语写作** | 技术术语用英文，解释说明用中文 |
| **交叉引用** | `[[文件名\|显示文字]]`，跨模块用 vault 相对路径，不写 `.md` 后缀 |
| **YAML frontmatter** | 不使用 |
| **Tags** | 不使用 Obsidian `#tag` 语法 |
| **图片引用** | `![描述](picture/xxx.png)`，统一 `.png` 后缀 |

**新建笔记默认**采用「单文件双分区」格式（同一 `.md` 内）；用户明确选择「仅提纲/仅详情」时可在方案中标注例外：

- `## 【核心精简提纲】` — 要点、清单、结论
- `## 【完整拓展详情】` — 原理、案例、踩坑、wikilink

### 4. 方案展示与用户确认

在按计划执行所有文件操作之前，向用户展示完整的「摄入计划」：

```
📋 摄入计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
① [新建] C-Linux生态/01.Linux环境/6. 网络工具.md
   ← curl/wget/ss/iperf 等网络工具用法 · 3 个代码块 · 1 张表

② [扩展] C-Linux生态/01.Linux环境/8. 常用指令.md
   ← 追加 tcpdump 常用参数段落

③ [wikilink] 链接到 [[4. perf|perf 笔记]] 等已有笔记

④ [删除] raw/待清洗数据.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
? 确认执行上述初步方案？[Y/e/n]
```

- `Y` → 执行
- `e` → 编辑（用户可以补充调整意见）
- `n` → 取消

### 5. 执行文件操作

按确认后的方案执行：

- **新建文件**：用 `Write` 在目标目录创建 `.md` 文件
- **扩展现有文件**：用 `Write` / `StrReplace` 追加或插入内容
- **补 wikilink**：与同模块/跨模块相关笔记互链
- **确保 `.gitkeep`**：目录变更后运行：
  ```powershell
  powershell -File .git\hooks\auto-gitkeep.ps1
  ```
  脚本不存在时按 [CLAUDE.md](../../CLAUDE.md) Maintain Directories 内联 PowerShell 命令回退- **图片引用**：如果内容中引用了图片但 `picture/` 下无对应文件，提示用户

### 6. 更新索引文件

#### `.claude/instructions/01-repo-structure.md`

- 更新受影响目录的笔记计数（每新增 1 篇 +1）
- 更新目录描述中的笔记列表（追加新笔记的标题摘要）
- 更新总笔记数

#### `README.md`

- 更新 `📂 目录结构` 中受影响目录的注释描述
- 更新 `✨ 专题一览` 表格（如果新内容引入新主题方向，更新对应列的描述）

- 更新 `readme/README_EN.md` 对应段落（若目录结构描述变更）

### 7. 删除原始数据文件

- 如果输入来自文件路径，用 `git rm` 删除源文件
- 如果输入来自粘贴内容，跳过此步
- 仅删除已确认处理完毕、内容已完全摄入的源文件

### 8. 提交前自检与 Git 提交

commit 前依 [06-continuous-review.md](../../instructions/06-continuous-review.md) 对变更 `.md` 做 7 项审查（标题、frontmatter/tag、代码块标注、wikilink、双语、交叉引用、图片路径），并运行：

```bash
git add --renormalize .
```

**Git commit 仅在你明确要求时执行**（否则停在「文件已写入、待提交」状态）。

未在本 Skill 内提交时，结束语须包含：

> 笔记与索引已写入。运行 `/quick-commit` 可分析全部改动（含 `git rm` 的源文件删除）并生成逐文件详细 commit message。

**不要**只 stage 部分文件后结束；要么用户明确要求时完整 `git add` + commit，要么全部留给 `/quick-commit`。

用户要求提交时，先 `git add` 纳入变更，再：

```bash
git add --renormalize .
```

#### commit 策略

| 情况 | 策略 |
|------|------|
| 用户未要求提交 | 不 commit，提示 `/quick-commit` |
| 用户要求提交且改动集中 | 1 次 commit（可扼要 1 行，或展开 bullet） |
| 用户要求提交且改动跨多目录 | **推荐** `/quick-commit` 生成逐文件详细 log；勿自动多次 commit |
#### commit message 格式

```
type(scope): 本次改动的核心内容

- 具体变更项列表（每个文件一行）
  ...
```

- **type**: `docs`（笔记内容类），`feat`（实质知识新增）
- **scope**: 受影响的主要目录缩写（`c-lang`, `C++`, `linux`, `E-AI`, `vault` 等）
- **description**: 简述本次**实际改动**（新增/拓展/修改/删除），不提及"拆分/清洗/摄入"过程
- **列表项**：每个文件一行，用项目符号列出具体操作

示例：
```
docs(C-Linux): 新增「网络工具」笔记，拓展「常用指令」curl 章节

- 新建 01.Linux环境/6. 网络工具.md 覆盖 curl/wget/ss/iperf 用法
- 扩展 01.Linux环境/8. 常用指令.md 追加 tcpdump 段落
- 删除已处理的源文件 raw/foo.md
```

---

## 边界条件处理

| 场景 | 处理方式 |
|------|----------|
| 输入内容为空 | 提示用户并退出 |
| 内容与现有所有笔记无关 | 写入 `待记录专题.md` backlog，或与用户确认新建子目录 |
| 内容全是代码无说明 | 按"代码片段"格式整理，加标题 + 中文注释解释用途 |
| 目标目录不存在 | 按项目规范创建目录，写入 `.gitkeep` |
| 新建文件数字冲突 | 扫描目标目录 `.md` 文件，取最大数字序号 +1 作为新文件序号 |
| 内容非常长（>200 行） | 考虑按子主题拆分为多篇笔记，在方案中说明 |
| 主题太大、一次写不完 | 先写双分区提纲区，详情区分批补充；或记入 `待记录专题.md` |
| 有配图但未提供 | 先留 `![描述](picture/xxx.png)` 占位并提示用户补图 |
| 源文件部分内容未处理 | 保留源文件，在方案中说明哪些内容未被摄入及原因，询问用户是否仍要删除 |

---

## 使用时机

- 从网页/书籍/对话中收集了零散知识点，需要统一格式入库时
- 拿到了一份非结构化的笔记草稿需整理为标准笔记时
- 需要将内容合理分配到知识库中多个相关笔记时

## 注意事项

1. **不将拆分过程写入 commit** — commit log 只反映"新增/拓展/修改/删除了什么"
2. **严格遵守标题编号规则** — 文件内从 `# 1.` 开始，文件序号与标题序号无关
3. **跨目录操作时先综览再动手** — 先读取 README 和目录结构再制定方案
4. **Commit 前展示方案** — 必须让用户确认后再执行，不静默操作
5. **使用项目规定的 shell 策略** — 优先 Git Bash，中文乱码时回退 PowerShell 并设 `LC_ALL=C.UTF-8`
6. **Plan 模式落盘** — Plan 模式下必须按 [07-plan-mode.md](../../instructions/07-plan-mode.md) 写入 `.claude/plan/`；非 Plan 模式的复杂摄入可选手写计划快照

## 工作流衔接

| 方向 | Skill |
|------|-------|
| 下一步（默认） | [/quick-commit](../quick-commit/SKILL.md) — 分析全部改动并提交 |
| 推送前 | [/squash-commits](../squash-commits/SKILL.md) — 合并多次中间态 commit |

## 相关文件

- [02-note-conventions.md](../../instructions/02-note-conventions.md)
- [01-repo-structure.md](../../instructions/01-repo-structure.md)
- [03-git-workflow.md](../../instructions/03-git-workflow.md)
- [06-continuous-review.md](../../instructions/06-continuous-review.md)
- [07-plan-mode.md](../../instructions/07-plan-mode.md)
