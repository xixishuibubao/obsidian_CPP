---
name: vault-audit
description: Runs full or incremental mechanical audits plus per-module semantic review, outputs audit reports, and fixes by P0/P1/P2 priority. Use when auditing the vault, scanning broken links, or invoking /vault-audit.
disable-model-invocation: true
---

# /vault-audit — 知识库审计

模式、M1–M10、语义审查、报告格式见 [08-vault-audit.md](../../instructions/08-vault-audit.md)。

## 脚本（Python 优先）

```bash
python .claude/skills/vault-audit/scripts/vault-audit.py full
python .claude/skills/vault-audit/scripts/vault-audit.py quick --json
bash .claude/skills/vault-audit/scripts/vault-audit.sh quick   # 包装
```

陈旧词表：编辑 `scripts/vault-audit.py` 内 `STALE_KEYWORDS`。

## 执行流程

### 1. 扫描

vault 根目录运行上述命令（`full` / `quick` / `module:<path>`）。

### 2. 报告

更新 `.claude/plan/YYYY-MM-DD-vault-audit-report.md`（模板：[templates/vault-audit-report.template.md](templates/vault-audit-report.template.md)）。

### 3. 用户确认

```
? 如何处理审计结果？[Y/e/n/s]  （见 README §用户确认协议）
```

- **推送门禁**：P0>0 时警告不建议 push
- **修复环退出**：P0=0 且 quick 重跑通过 → squash；最多 2 轮

### 4. 修复 → 5. 提交

按 [08-vault-audit.md](../../instructions/08-vault-audit.md) P0/P1/P2 批次修复；完成后 `/quick-commit`（§B 见 [03-git-workflow.md](../../instructions/03-git-workflow.md)）。

## 工作流衔接

| 方向 | Skill |
|------|-------|
| 上游 | [/quick-commit](../quick-commit/SKILL.md) |
| 下游 | [/quick-commit](../quick-commit/SKILL.md) → [/squash-commits](../squash-commits/SKILL.md) |

维护链见 [README §知识库维护链](../README.md#知识库维护链)。

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)。优先用 `python vault-audit.py`。

## 参考

- [08-vault-audit.md](../../instructions/08-vault-audit.md)
- [06-continuous-review.md](../../instructions/06-continuous-review.md)
