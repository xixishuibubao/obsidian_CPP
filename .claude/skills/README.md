# 项目 Skill 索引

路径：`.claude/skills/<name>/SKILL.md`（可选 `scripts/` 子目录放 Skill 专用脚本）。Claude Code 用 `/name` 调用；Cursor 等 Agent 读取对应 `SKILL.md` 等效执行。

> **自包含**：脚本与 Skill 文档同目录，不单独放在 `.claude/scripts/`。

## 知识库维护链（日常）

```
收集 → /ingest-note → /quick-commit → [/vault-audit quick] → /squash-commits → push
```

| Skill | 定位 | 下一步 |
|-------|------|--------|
| [ingest-note](ingest-note/SKILL.md) | 清洗原始文本 → 格式化 → A–G 落盘 → 索引 | `/quick-commit` |
| [quick-commit](quick-commit/SKILL.md) | 分析 diff → 逐文件 Conventional Commit | `/vault-audit quick` 或 `/squash-commits` |
| [vault-audit](vault-audit/SKILL.md) | 断链/索引/格式/陈旧词表 + 分模块语义审查 | `/quick-commit` |
| [squash-commits](squash-commits/SKILL.md) | 合并本地 commits、清理备份提交 | 用户 `git push` |

## 环境初始化链（一次性）

推荐顺序：`init-win-env` → `init-git-convention` → `init-note-vault`

| Skill | 定位 |
|-------|------|
| [init-win-env](init-win-env/SKILL.md) | Windows：探测 Git Bash/PowerShell、Shell 规则、权限 |
| [init-git-convention](init-git-convention/SKILL.md) | 注入 Conventional Commits 与 Git 工作流 |
| [init-note-vault](init-note-vault/SKILL.md) | Obsidian/Markdown 笔记规范初始化 |

## 权威对照

- [05-agent-coordination.md](../instructions/05-agent-coordination.md) — Cursor 等效步骤
- [03-git-workflow.md](../instructions/03-git-workflow.md) — Commit / squash 细则
- [[E-AI与Agent协同开发/03.工具与配置/5. Claude Code Skill 能力总览与推荐清单|Skill 能力总览笔记]]
