# 多 Agent 协作约定

## 1. 主 Agent

本仓库以 **Claude Code** 为主 Agent。项目级规则、笔记规范、Git 工作流均以 Claude Code 侧维护的文件为权威来源。

| 角色 | 工具 | 权威配置 |
|------|------|----------|
| 主 Agent | Claude Code | `CLAUDE.md`、`.claude/instructions/`、Claude Code 项目记忆 |
| 辅助 Agent | Cursor、其他 IDE Agent | 须对齐上表；规则见 `.cursor/rules/claude-code-primary.mdc` |

## 2. Cursor / 其他 Agent 开工 checklist

1. 阅读根目录 **`CLAUDE.md`**
2. 按任务类型阅读 `.claude/instructions/` 子文件：
   - 写/改笔记 → `02-note-conventions.md`
   - 提交/推送 → `03-git-workflow.md`
   - 目录规划 → `01-repo-structure.md`
3. 查看 **`待记录专题.md`** 与近期 `git log`，了解 Claude Code 侧未完成或刚完成的工作
4. 仅在用户明确要求时 commit；消息格式遵循 `03-git-workflow.md`

## 3. 约定同步

- 在 Cursor 中形成的新约定（命名、流程、禁忌）应 **回写** `CLAUDE.md` 或 `.claude/instructions/`，供 Claude Code 下次会话读取
- 避免 Cursor 与 Claude Code 各维护一套冲突规则
- `CLAUDE.md` 保持简洁（150~180 行）；细则放 `.claude/instructions/` 子文件

## 4. Claude Code Skills 映射

Cursor 无 slash command 时，手动执行等效步骤：

| Skill | 等效操作 |
|-------|----------|
| `/ingest-note` | 清洗文本 → 按 `02-note-conventions.md` 格式化 → 分类落盘 → 更新 wikilink → 用户确认后 commit |
| `/quick-commit` | `git status` / `git diff` → Conventional Commit → 用户确认后 commit |
| `/squash-commits` | `git rebase -i` 或 soft reset 合并本地 commits（推送前） |

## 5. 相关文件

- [CLAUDE.md](../../CLAUDE.md)
- [02-note-conventions.md](02-note-conventions.md)
- [03-git-workflow.md](03-git-workflow.md)
- `.cursor/rules/claude-code-primary.mdc`
- 关于 Claude Code Team 模式（多 Agent 团队成员协作）参见 [[E-AI与Agent协同开发/03.工具与配置/3. Claude Code Team 模式协作指南|Team 模式协作指南]]
