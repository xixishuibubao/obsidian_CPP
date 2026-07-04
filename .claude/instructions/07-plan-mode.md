# Plan 模式与计划文件

## 存放位置（强制）

Cursor / Claude Code 等 Agent 在 **Plan 模式**下产出的思考与计划文件，**必须**写入仓库内：

```
.claude/plan/
```

| 要求 | 说明 |
|------|------|
| **唯一落盘目录** | 仅 `.claude/plan/`，不得写入 `.cursor/plans/`、系统临时目录或 vault 外路径 |
| **与笔记分离** | 计划文件不是 Obsidian 笔记，不放入 A–G 模块目录 |
| **可追溯** | 计划执行完毕后**保留**文件供回顾；过时计划由用户手动清理 |
| **空目录** | 无 plan 文件时保留 `.gitkeep` 占位 |

## 文件命名

```
YYYY-MM-DD-简短主题.plan.md
```

示例：`.claude/plan/2026-07-04-新知识入库流程.plan.md`

- 日期为创建日（本地时区）
- 主题用简体中文或英文短语，避免空格（用连字符 `-`）
- 后缀固定 `.plan.md`，与 vault 笔记 `.md` 区分

## 内容格式

计划文件为 **Agent 工作产物**，不受 vault 笔记规范约束（可有 YAML frontmatter、`#tag` 等），但建议：

```markdown
---
name: 计划标题
overview: 一两句摘要
status: draft | confirmed | done | cancelled
created: YYYY-MM-DD
---

# 计划标题

## 背景与目标
…

## 方案
…

## 待办
- [ ] …
```

Plan 模式若通过工具生成带 `todos` frontmatter 的文件，落盘时保持该结构即可。

## Agent 工作流

1. **生成计划时**：直接在 `.claude/plan/` 创建或更新对应 `.plan.md`，不在对话外静默落盘到其他路径
2. **用户确认后执行**：在同一文件更新 `status: done`（或 `cancelled`），可选追加「执行摘要」小节
3. **多轮修订**：优先编辑同一计划文件，而非新建重复主题文件
4. **Git**：计划文件**可**随其他改动一并提交；无用户要求时不单独 commit

## 与其他目录的关系

| 路径 | 用途 |
|------|------|
| `.claude/instructions/` | 长期有效的项目规范（本文件所在处） |
| `.claude/plan/` | 单次任务/会话的计划与思考快照；语义 backlog 见 `*-vault-audit-report.md` |
| `.claude/skills/` | 可复用的 slash command 工作流 |

## 相关文件

- [CLAUDE.md](../../CLAUDE.md) — Key Rules 摘要
- [05-agent-coordination.md](05-agent-coordination.md) — 多 Agent 协作
