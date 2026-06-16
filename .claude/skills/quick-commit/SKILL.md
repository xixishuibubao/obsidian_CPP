---
name: quick-commit
description: 自动 stage 所有改动 → 分析 diff → 检测外部手动修改 → 生成 Conventional Commit → 确认后执行
---

# /quick-commit — 快速提交

分析当前所有改动（含 AI 生成与外部的修改），自动生成 Conventional Commit 并执行。

---

## 执行流程

### 1. 入口预检

```bash
git status --short            # 完整状态：暂存区 + 工作区 + 未跟踪文件
git diff --cached --stat      # 已暂存的变更
git diff --stat               # 未暂存的变更（外部手动修改候选）
```

根据结果分支处理：

| 暂存区 | 工作区/未跟踪 | 行为 |
|--------|--------------|------|
| 有内容 | 有改动 | 继续流程，进入【手动改动检测】 |
| 有内容 | 空 | 继续流程，仅含 AI 侧改动 |
| 空 | 有改动 | 提示"暂存区为空，是否自动 `git add -A` 后继续？[Y/n]" |
| 空 | 空 | 提示"无任何改动，无需提交"，退出 |

> **设计依据**：典型的混合场景是——AI 做完改动后 `git add` 了部分文件，你又在 Obsidian/编辑器中手动改了其他文件，此时暂存区和工作区都有内容。

### 2. 手动改动检测

从 `git status --short` 中识别未暂存的变动文件（第二列为 `M`/`D`/`?` 等标记），这些可能是你在外部工具中手动修改的。

如果有检测到，展示并询问：

```
🔍 改动来源检测
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [暂存区]  AI 侧改动（已 stage）:
    M  E-AI与Agent协同开发/.../6. Skill 工程化能力自评与进阶路线.md
    A  E-AI与Agent协同开发/.../7. 新笔记.md

  [未暂存]  可能为外部手动修改:
    M  C-Linux生态/01.Linux环境/8. 常用指令.md    ← 手动修改
    ?? raw/临时笔记.md                              ← 新建文件

? 检测到未暂存的改动，是否将这些外部修改合并到本次提交？
   [Y] 是，合并提交，log 统一概括所有改动
   [n] 否，只提交已暂存的 AI 改动
   [s] 跳过，我先手动处理这些文件
```

- `Y` → `git add -A` 纳入所有改动，统一分析
- `n` → 仅分析暂存区内容，工作区改动保持不变
- `s` → 清除暂存区（`git reset`），本次不提交，留给用户自行处理

### 3. 分析变更（Schema 约束）

```bash
# 根据上一步的选择，分析全部或仅暂存区的 diff
git diff --cached --stat      # 变更文件列表及行数统计
git diff --cached             # 完整变更内容
```

使用以下 Schema 约束分析结果格式：

```
分析结果 Schema:
{
  type: "feat" | "fix" | "docs" | "style" | "refactor" | "perf" | "test" | "chore",
  scope: string,              // 从目录名推断，如 "c-lang", "linux", "E-AI"
  description: string,        // 中文优先，概括改动的核心内容
  changes: [                   // 每个改动的具体描述
    {
      file: string,           // 文件路径
      action: "added" | "modified" | "deleted",
      source: "ai" | "manual" | "mixed",  // 改动来源（AI 生成/外部手动）
      summary: string         // 该文件的改动摘要
    }
  ],
  manual_summary: string | null,  // 外部手动改动的总体描述，无手动改动则为 null
  notes: string | null        // 特别说明（如需要用户注意的事项），无则为 null
}
```

分析依据：

| 分析项 | 判断依据 |
|--------|----------|
| **type** | 新增笔记内容 → `docs`，修复 typo → `fix`，新增代码 → `feat`，格式调整 → `style`，配置改动 → `chore`，目录/文件移动 → `refactor` |
| **scope** | 从改动的文件目录名提取（`.claude/` → `claude`, `C-Linux生态/` → `linux`, `src/` → `src`） |
| **description** | 从 diff 摘要生成核心概括，中文优先，**必须体现具体改动内容**，不得使用"若干""一些""多处"等模糊表述 |
| **source** | 来自暂存区 → `ai`，来自未暂存区的询问后纳入 → `manual`，两者混合 → `mixed` |

### 4. 生成 Commit Message

格式：
```
type(scope): 核心概括（≤ 50 字，中文优先）

- 文件1：具体改动了什么、为什么
- 文件2：具体改动了什么、为什么
- 文件3：具体改动了什么、为什么
```

**核心要求（遵循项目 CLAUDE.md 规范）：**
- description 必须简述具体改动点，不得过度概括导致信息丢失
- 每个变更文件至少对应一条 bullet point，写明该文件的实际改动内容
- 合并改动时（如同时更新了笔记 + 索引），在 bullet point 中体现文件间的关系
- 当有手动改动时，description 后缀 `+ 手动...`，并在 bullet point 中标注

示例（纯 AI）：
```
docs(E-AI): 新增 Skill 总览笔记，同步更新仓库结构索引与笔记计数

- .claude/instructions/01-repo-structure.md：E-AI 模块笔记计数 4→5，总笔记数 96→97，目录描述追加 Skill 总览条目
- 03.工具与配置/5. Claude Code Skill 能力总览与推荐清单.md：新建笔记，系统梳理 6 类 Skill 能力与选型建议
- 03.工具与配置/1. 工具与配置索引.md：追加 Skill 总览笔记链接到索引文章列表
```

示例（混合手动改动）：
```
docs(linux): 新增 ssh 免密登录笔记，补充常用指令条目 + 手动修正格式

- 01.Linux环境/8. 常用指令.md：新增 ssh-keygen/ssh-copy-id 条目及参数说明
- 01.Linux环境/9. ssh免密登录.md：新建笔记，覆盖密钥生成、分发、agent 配置全流程
- 02.C++/3. 代码规范.md：修正拼写错误与缩进格式（manual）
```

**生成规则：**
- 第一行 `type(scope): 概括` 与第 3 步 Schema 中的 `type`/`scope`/`description` 一致
- 后续 bullet point 由 Schema 中 `changes[].summary` 逐条展开，补充「做了什么」而非仅「哪个文件变了」
- 多条修改有因果关联时，合并为一条 bullet 描述，避免碎片化

### 5. 展示确认

展示分析结果与生成的 commit message，标明改动来源：

```
📋 提交计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  类型:    docs
  范围:    linux
  ──
  Commit Message:
  docs(linux): 新增 ssh 免密登录笔记，补充常用指令条目 + 手动修正格式

  - 01.Linux环境/8. 常用指令.md：新增 ssh-keygen/ssh-copy-id 条目及参数说明 (ai)
  - 01.Linux环境/9. ssh免密登录.md：新建笔记，覆盖密钥生成、分发、agent 配置全流程 (ai)
  - 02.C++/3. 代码规范.md：修正拼写错误与缩进格式 (manual)
  ──
  手动改动摘要:
    - 调整代码规范中的格式和错别字

? 确认执行提交？[Y/e/n]
```

用户可选择：
- `Y` → 直接执行 `git commit -m "type(scope): description"`
- `e` → 输入自定义 commit message 后执行
- `n` → 取消，不清除暂存区

### 6. 执行

```bash
# 多行 commit message：第一行为标题，后续为 body（bullet points）
git commit -m "$header" -m "$body"
```

其中 `$header` = `type(scope): 核心概括`，`$body` = 逐条 bullet point 列表（用空行与 header 隔开）。

当 body 较长时，也可写入临时文件后执行：
```bash
git commit -t /dev/stdin <<EOF
type(scope): 核心概括

- 改动项 1
- 改动项 2
EOF
```

### 7. 提交后验证

```bash
git log --oneline -3          # 展示最近 3 条提交，确认新提交在顶端
```

验证后展示给用户：

```
✓ 提交成功:
  a1b2c3d docs(linux): 新增 ssh 免密登录笔记，补充常用指令条目 + 手动修正格式

  - 01.Linux环境/8. 常用指令.md：新增 ssh-keygen/ssh-copy-id 条目及参数说明 (ai)
  - 01.Linux环境/9. ssh免密登录.md：新建笔记，覆盖密钥生成、分发、agent 配置全流程 (ai)
  - 02.C++/3. 代码规范.md：修正拼写错误与缩进格式 (manual)

  本次提交包含 AI 生成改动 + 外部手动修改
```

如果提交失败（hooks 拒绝、合并冲突等），展示错误信息并给出修复建议。

## 使用时机

- 完成一次改动后，准备记录进度时
- 在 Obsidian/编辑器中手动修改文件后，与 AI 改动一起提交时
- 无需关心 stage 粒度，只想「全部提交」时

## 注意事项

- **不跳过 pre-commit hooks** — 尊重项目配置
- 如果项目 CLAUDE.md 中定义了 Git 规范，优先使用项目规范；否则使用全局默认
- commit message 语言遵循项目 CLAUDE.md 中的设置，如未设置则使用中文
- 如果暂存区和工作区都为空，提前退出
- **手动改动检测**依赖未暂存状态识别——如果你已经手动 `git add` 了所有文件，skill 无法区分哪些是手动改的，会全部标记为 `ai`
- 提交失败时展示具体错误，不静默失败
- `source` 标记仅在展示和确认时可见，不会写入 commit message 本身
- **Commit message 必须详细**：每个文件至少一条 bullet point 描述具体改动，不得只有一行概括。遵循项目 CLAUDE.md 中"不得过度概括导致信息丢失"的规则
