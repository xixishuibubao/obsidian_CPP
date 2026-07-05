# 项目 Skill 索引

路径：`.claude/skills/<name>/SKILL.md`（可选 `scripts/`、`templates/`、`reference.md`）。Claude Code 用 `/name` 调用。

> **自包含**：脚本与 Skill 文档同目录，不单独放在 `.claude/scripts/`。
> **脚本优先级**（可实现时）：**Python > Bash > PowerShell > CMD**；主逻辑在 `.py`，`.sh`/`.ps1` 为薄包装。

## Cursor 等效调用（全 Skill 通用）

无 `/name` slash command 时，读取 `.claude/skills/<name>/SKILL.md` 并按步骤执行。Shell/脚本约束见各 Skill 顶部或 [04-shell-config.md](../instructions/04-shell-config.md)、[09-toolchain-config.md](../instructions/09-toolchain-config.md)。

## 用户确认协议（全 Skill 通用）

| 键 | 含义 |
|----|------|
| `Y` | 确认，按方案执行 |
| `e` | 编辑方案后再确认（README 默认）；**quick-commit 空暂存区时** `e`=指定纳入路径 |
| `n` | 取消，不改动或保留当前 Git 状态 |
| `s` | 跳过本步（quick-commit 手动改动、squash 脏工作区 stash、vault-audit 跳过修复） |

**场景扩展**：squash 脏工作区用 `[s] stash / [c] cancel`；quick-commit 手动改动检测用 `[Y/n/s]`。

## 知识库维护链（日常）

```
收集 → /ingest-note → /quick-commit → [/vault-audit quick] → /squash-commits → push
```

| Skill | 定位 | 下一步 |
|-------|------|--------|
| [ingest-note](ingest-note/SKILL.md) | 清洗 → A–G 落盘 → 索引 | `/quick-commit` |
| [quick-commit](quick-commit/SKILL.md) | diff → §B Conventional Commit | 入库后 `/vault-audit quick`；推送前 `/squash-commits` |
| [vault-audit](vault-audit/SKILL.md) | 机械审计 + 分模块语义 | 修复后 `/quick-commit` |
| [squash-commits](squash-commits/SKILL.md) | 合并本地 commits | 用户 `git push` |

**何时跑 vault-audit quick**：笔记入库后、跨模块改动后、push 前（P0 须清零）。Cursor 等效步骤见 [05-agent-coordination.md](../instructions/05-agent-coordination.md) §4。

## 环境初始化链（一次性）

```
init-win-env → probe-toolchain → init-git-convention → init-note-vault
```

| Skill | 定位 |
|-------|------|
| [init-win-env](init-win-env/SKILL.md) | Shell 策略 + 04-shell-config + 基础权限 |
| [probe-toolchain](probe-toolchain/SKILL.md) | Tier 1 工具路径 → toolchain.json |
| [init-git-convention](init-git-convention/SKILL.md) | Git 工作流 + 03-git-workflow |
| [init-note-vault](init-note-vault/SKILL.md) | 笔记规范 + 02-note-conventions |

## 权威对照

- [05-agent-coordination.md](../instructions/05-agent-coordination.md) — Cursor checklist
- [03-git-workflow.md](../instructions/03-git-workflow.md) — Commit / squash
- [06-continuous-review.md](../instructions/06-continuous-review.md) — 7+4 审查、renormalize、hook
- [08-vault-audit.md](../instructions/08-vault-audit.md) — M1–M10
- [09-toolchain-config.md](../instructions/09-toolchain-config.md) — 工具链 pin
