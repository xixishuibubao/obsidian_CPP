---
name: vault-audit
description: 全库/增量机械审计 + 分模块语义审查，生成 audit-report，按 P0/P1/P2 修复。Use when /vault-audit、知识库审计、断链扫描、索引漂移
---

# /vault-audit — 知识库审计

扫描 Obsidian vault 的机械项（断链、索引、格式、陈旧词表）与分模块语义问题，产出报告并按优先级修复。

---

## 脚本（Skill 自包含）

本 Skill 脚本位于同目录 `scripts/`：

- `scripts/vault-audit.sh` — 机械审计主脚本

```bash
bash .claude/skills/vault-audit/scripts/vault-audit.sh full
```

---

## 模式

| 模式 | 命令 | 用途 |
|------|------|------|
| `full` | `/vault-audit full` | 首次基线 + 季度全库（M1–M9） |
| `quick` | `/vault-audit quick` | push 前快检（M1/M2/M3/M9） |
| `module:<path>` | `/vault-audit module:C-Linux生态/01.Linux环境` | 单模块语义逐篇审查 |

---

## 执行流程

### 1. 扫描

```bash
cd <vault-root>
bash .claude/skills/vault-audit/scripts/vault-audit.sh full          # 或 quick / module:PATH
bash .claude/skills/vault-audit/scripts/vault-audit.sh full --json   # 机器可读
```

### 2. 报告

- 更新或创建 `.claude/plan/YYYY-MM-DD-vault-audit-report.md`
- 摘要：P0/P1/P2 计数
- 机械项清单（`- [ ]` / `- [x]`）
- 分模块语义审查表（A–G 各子目录，结论：`ok` / `fixed` / `backlog`）
- 修复批次与 commit 引用
- S3 未决项 → 写入 `.claude/plan/*-vault-audit-report.md`「未决项」章节

报告模板见同目录最新 `*-vault-audit-report.md`。

### 3. 用户确认 → 修复

按严重度批次处理：

| 级别 | 内容 | 策略 |
|------|------|------|
| P0 | M1 断链 wikilink、M2 图片断链 | 必须清零 |
| P1 | M3 索引、M5/M6 格式、M9 陈旧词表 | 基线阶段尽量清零 |
| P2 | M7 序号、M8 孤立 | 结构审计阶段处理 |

修复后重跑 `vault-audit.sh` 验证，更新 report 勾选状态。

### 4. 语义审查（module 模式）

对子目录内每篇笔记核对：

1. **事实性** — 命令/选项/API 是否仍正确
2. **上下文** — 是否仍绑定已删除工程（改通用示例）
3. **完整性** — 双分区是否齐全；提纲与详情是否一致
4. **交叉引用** — 是否链到同模块互补笔记
5. **索引一致** — 模块描述与笔记标题是否一致

分级：S1 明显错误→当次修复；S2 过时→加日期标注或改通用表述；S3 需重写→audit-report「未决项」。

### 5. 提交

修复批次完成后提示 `/quick-commit`：

- B0 基础设施：`feat(claude): 新增 vault-audit Skill 与审计脚本`
- B1 机械项：`fix(vault): 基线审计修复断链与索引漂移`
- 结构：`refactor(vault): …`
- 语义：`docs(<模块>): 审计修正 …`

---

## 与维护链关系

```
ingest-note → quick-commit → [vault-audit quick] → squash-commits → push
```

- **ingest-note**：落盘前 M7 序号扫描；入库后更新索引
- **quick-commit**：对已 stage 的 `.md` 跑增量 7+4 项（见 `06-continuous-review.md`）
- **vault-audit quick**：push 前 M1/M2/M3/M9
- **vault-audit full**：季度或重大目录变更后

细则：[08-vault-audit.md](../../instructions/08-vault-audit.md)

---

## 参考

- [01-repo-structure.md](../../instructions/01-repo-structure.md) — 目录语义与计数
- [02-note-conventions.md](../../instructions/02-note-conventions.md) — wikilink 规则
- [06-continuous-review.md](../../instructions/06-continuous-review.md) — 增量审查 7+4 项
