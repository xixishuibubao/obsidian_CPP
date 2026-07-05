---
name: init-note-vault
description: Initializes Obsidian/Markdown vault note conventions in default or minimal mode. Use when creating a new knowledge base or invoking /init-note-vault.
disable-model-invocation: true
---

# /init-note-vault — 笔记知识库规范初始化

为 Obsidian / Markdown 知识库初始化笔记规范。模板见 [reference.md](reference.md)。

---

## 执行流程

### 0. 预检与冲突检测

检查 `CLAUDE.md`、`.claude/instructions/`、`02-note-conventions.md` 是否已存在；冲突时询问追加/覆盖/跳过。

### 1. 询问模式

- **默认模式**：完整规则集（标题编号、wikilink、无 frontmatter、代码块、双语…）
- **精简模式**：最小规则集，可后续升级

### 2. 询问模板参数（多选）

- 完整性检查命令
- 语言标注列表（全量 11 种 / 精简 5 种）
- `.gitkeep` 维护脚本段落

### 3–5. 生成文件

| 输出 | 说明 |
|------|------|
| `CLAUDE.md` | Quick Reference + Key Rules + Directory Structure（reference.md） |
| `.claude/instructions/02-note-conventions.md` | 扫描编号；本 vault 已有权威版以合并为主 |

### 6. 验证

确认 Quick Reference 与 instructions 文件存在。

> 笔记规范已就绪。维护链入口：`/ingest-note`

## Bootstrap

`init-win-env` → `probe-toolchain` → `init-git-convention` → **init-note-vault**（第四步）

单独补跑本 Skill 时无需再跑 init-git-convention。

## 注意事项

- 目录结构表用通用占位，不绑定具体科目
- instructions 编号动态扫描

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)

## 相关文件

- [reference.md](reference.md)
- [02-note-conventions.md](../../instructions/02-note-conventions.md)
- [../init-git-convention/SKILL.md](../init-git-convention/SKILL.md)
