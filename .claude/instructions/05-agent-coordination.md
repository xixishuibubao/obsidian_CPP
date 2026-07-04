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
5. Plan 模式任务 → 阅读 `07-plan-mode.md`；计划文件写入 `.claude/plan/`

## 3. 约定同步

- 在 Cursor 中形成的新约定（命名、流程、禁忌）应 **回写** `CLAUDE.md` 或 `.claude/instructions/`，供 Claude Code 下次会话读取
- 避免 Cursor 与 Claude Code 各维护一套冲突规则
- `CLAUDE.md` 保持简洁（150~180 行）；细则放 `.claude/instructions/` 子文件

## 4. Claude Code Skills 映射

Skill 索引见 [`.claude/skills/README.md`](../skills/README.md)。Cursor 无 slash command 时，读取对应 `SKILL.md` 等效执行。

### 知识库维护链

```
ingest-note → quick-commit → squash-commits → push
```

| Skill | 路径 | 等效操作 |
|-------|------|----------|
| `/ingest-note` | `.claude/skills/ingest-note/SKILL.md` | 清洗→格式化→A–G 落盘→wikilink→索引/README→删源→06 审查→renormalize→可选 commit |
| `/quick-commit` | `.claude/skills/quick-commit/SKILL.md` | status/diff/log→手动改动检测→06 审查→renormalize→逐文件 Conventional Commit→确认 commit |
| `/squash-commits` | `.claude/skills/squash-commits/SKILL.md` | 工作区预检→列未推送 commits→备份检测→策略→renormalize→squash→diff 验证 |

### 环境初始化链（一次性）

推荐顺序：`init-win-env` → `init-git-convention` → `init-note-vault`

| Skill | 路径 | 等效操作 |
|-------|------|----------|
| `/init-win-env` | `.claude/skills/init-win-env/SKILL.md` | 探测 bash/git→Shell 规则→04-shell-config→settings 权限 |
| `/init-git-convention` | `.claude/skills/init-git-convention/SKILL.md` | git 预检→Git 段落→NN-git-workflow.md→settings 权限 |
| `/init-note-vault` | `.claude/skills/init-note-vault/SKILL.md` | 冲突检测→默认/精简模式→CLAUDE.md + note-conventions |

## 5. Plan 模式

- 计划与思考文件 **仅** 落盘 [`.claude/plan/`](../plan/)
- 命名：`YYYY-MM-DD-简短主题.plan.md`
- 完整规则见 [07-plan-mode.md](07-plan-mode.md)
- 知识入库类 Plan 的权威 Skill 见 [ingest-note](../skills/ingest-note/SKILL.md)（`/ingest-note`），Plan 文件仅作快照，不另建平行 workflow

## 6. 相关文件

- [CLAUDE.md](../../CLAUDE.md)
- [02-note-conventions.md](02-note-conventions.md)
- [03-git-workflow.md](03-git-workflow.md)
- [07-plan-mode.md](07-plan-mode.md)
- [.claude/skills/README.md](../skills/README.md)
- `.cursor/rules/claude-code-primary.mdc`
- 关于 Claude Code Team 模式（多 Agent 团队成员协作）参见 [[E-AI与Agent协同开发/03.工具与配置/3. Claude Code Team 模式协作指南|Team 模式协作指南]]
