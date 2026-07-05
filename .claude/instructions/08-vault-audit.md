# Vault Audit 细则

全库/增量机械审计与分模块语义审查的操作细则。入口 Skill：[vault-audit](../skills/vault-audit/SKILL.md)（`/vault-audit`）。

---

## 脚本位置（Skill 自包含）

脚本优先级：**Python > Bash > PowerShell**。主逻辑在 `vault-audit.py`。

```bash
python .claude/skills/vault-audit/scripts/vault-audit.py full          # 或 quick / module:PATH
python .claude/skills/vault-audit/scripts/vault-audit.py quick --json
bash .claude/skills/vault-audit/scripts/vault-audit.sh full           # 包装：优先调 python
```

| 模式 | 检查项 | 用途 |
|------|--------|------|
| `full` | M1–M10 | 基线/季度全库 |
| `quick` | M1/M2/M3/M9/M10 | push 前快检 |
| `module:<path>` | M1/M2 + 人工语义 | 单模块逐篇审查 |

---

## 机械检查项

| ID | 检查 | 严重度 |
|----|------|--------|
| M1 | wikilink 断链（排除 shell `[[ ]]`、行内代码） | P0 |
| M2 | `picture/` 图片断链（排除占位 `xxx`） | P0 |
| M3 | 子目录笔记数 vs `01-repo-structure.md` | P1 |
| M5 | 首行一级标题须为 `# 1.` | P1 |
| M6 | 无 YAML frontmatter（仅首行 `---`）；开 fence 须带语言 | P1 |
| M10 | 表格行内 `[[路径\|显示]]` 别名（`|` 与列分隔符冲突） | P1 |
| M7 | 同目录序号冲突 | P2 |
| M8 | 孤立笔记（0 入链 0 出链） | P2 |
| M9 | 陈旧词表（Telescope1126、DriverSO 等） | P1 |

陈旧词表维护于 `skills/vault-audit/scripts/vault-audit.py` 内 `STALE_KEYWORDS` 列表。

---

## 语义审查（module 模式）

每篇核对：事实性 · 上下文（无已删工程绑定）· 双分区完整性 · 交叉引用 · 索引一致。

| 级别 | 处理 |
|------|------|
| S1 明显错误 | 当次修复 |
| S2 过时可参考 | 加日期标注或改通用表述 |
| S3 需重写 | 写入 `.claude/plan/*-vault-audit-report.md`「未决项」 |

---

## 报告

- 路径：`.claude/plan/YYYY-MM-DD-vault-audit-report.md`
- 摘要 P0/P1/P2 · 机械项勾选 · 分模块语义表 · 修复批次 commit

---

## 维护链

见 [skills/README.md §知识库维护链](../skills/README.md#知识库维护链)。vault-audit 位于 quick-commit 之后、push 之前。
