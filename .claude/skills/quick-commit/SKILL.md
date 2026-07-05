---
name: quick-commit
description: Analyzes git status/diff (AI and manual edits) and generates per-file Conventional Commits after user confirmation. Use when committing changes or the user invokes /quick-commit.
disable-model-invocation: true
---

# /quick-commit — 快速提交

分析当前所有改动（含 AI 生成与外部的修改），自动生成 Conventional Commit 并执行。

---

## 执行流程

### 1. 入口预检

```bash
git status --short            # 完整状态：暂存区 + 工作区 + 未跟踪文件
git log --oneline -5          # 对齐近期 commit 风格
git diff --cached --stat      # 已暂存的变更
git diff --stat               # 未暂存的变更（外部手动修改候选）
```

根据结果分支处理：

| 暂存区 | 工作区/未跟踪 | 行为 |
|--------|--------------|------|
| 有内容 | 有改动 | 继续流程，进入【手动改动检测】 |
| 有内容 | 空 | 继续流程，仅含 AI 侧改动 |
| 空 | 有改动 | 提示"暂存区为空，是否自动 `git add -A` 后继续？[Y/e/n]"（e=指定路径，n=取消） |
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
- `s` → 取消本次 quick-commit，**保留**暂存区与工作区不变，由用户自行处理后再调用

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

格式与示例见 [03-git-workflow.md](../../instructions/03-git-workflow.md) §B。

**本 Skill 额外要求**：

- description ≤ 50 字，中文优先，不得用「若干/多处」等模糊词
- 每个变更文件至少一条 bullet；手动改动时 description 后缀 `+ 手动...`
- Schema 中 `source` 仅用于展示，不写入 commit message

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
- `Y` → 执行 `git commit -m "$header" -m "$body"`（header + 逐文件 bullet body，符合 §B）
- `e` → 输入自定义 commit message 后执行
- `n` → 取消，不清除暂存区

### 5.5 提交前自检

1. 若尚未 stage：按第 2 步用户选择 `git add -A` 或仅暂存区
2. 对 staged `.md` 执行 [06-continuous-review.md](../../instructions/06-continuous-review.md) **7 项**（不含 9–11）
3. Renormalize 与 hook 禁令见 06 §Renormalize / §Git hook 禁令

### 6. 执行

```bash
# 多行 commit message：第一行为标题，后续为 body（bullet points）
git commit -m "$header" -m "$body"
```

其中 `$header` = `type(scope): 核心概括`，`$body` = 逐条 bullet point 列表（用空行与 header 隔开）。

当 body 较长时，在 **Git Bash** 下可用 heredoc：

```bash
git commit -F - <<'EOF'
type(scope): 核心概括

- 改动项 1
- 改动项 2
EOF
```

PowerShell 回退时用多个 `-m` 传 body：

```bash
git commit -m "type(scope): 核心概括" -m "- 改动项 1" -m "- 改动项 2"
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

如果提交失败（hooks 拒绝、合并冲突等），展示错误信息并给出修复建议。**禁止** `--no-verify` 或 `--amend` 重试（除非用户明确要求）。

### 7.1 提交后下一步（维护链）

| 条件 | 建议 |
|------|------|
| 刚完成笔记入库/跨模块改动 | 运行 `/vault-audit quick` 检查断链与索引 |
| 仅 typo/小修且 audit 近期已通过 | 可跳过 audit，直接 `/squash-commits` |
| 本地未推送 commit ≥ 2 或含 `vault backup:` | 运行 `/squash-commits` 后再 `git push` |

结束语模板：
> ✓ 已提交。建议：`/vault-audit quick`（入库后推荐）或 `/squash-commits`（准备推送时）。

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
- **Commit message 必须详细**：见 [03-git-workflow.md](../../instructions/03-git-workflow.md) §B
- hook / renormalize：见 [06-continuous-review.md](../../instructions/06-continuous-review.md)
- 中文 commit 前设 `LC_ALL=C.UTF-8`，见 [04-shell-config.md](../../instructions/04-shell-config.md)

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)

## 工作流衔接

| 方向 | Skill |
|------|-------|
| 上游 | [/ingest-note](../ingest-note/SKILL.md) 或任意改动 |
| 下游 | [/squash-commits](../squash-commits/SKILL.md) — 推送前整理多次 commit |

## 相关文件

- [03-git-workflow.md](../../instructions/03-git-workflow.md)
- [06-continuous-review.md](../../instructions/06-continuous-review.md)
- [CLAUDE.md](../../CLAUDE.md) — Pre-commit 自检
- [../ingest-note/SKILL.md](../ingest-note/SKILL.md)
- [../squash-commits/SKILL.md](../squash-commits/SKILL.md)
