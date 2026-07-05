# init-note-vault — 参考模板

## CLAUDE.md Quick Reference（默认模式）

```markdown
## Quick Reference

| Item | Rule |
|------|------|
| **Note Links** | Obsidian wikilink `[[file\|display text]]`；表格内禁止 `\|` 别名 |
| **Title Format** | `# 1.`, `## 1.1`, `### 1.1.1` numbered |
| **Frontmatter** | No YAML frontmatter or tags |
| **Code Blocks** | Fenced with language annotation |
| **Images** | `![description](picture/filename.png)` |
| **Style** | Bilingual: English terms, {explanatory_language} explanation |
| **Empty Dirs** | `.gitkeep` placeholder files |

## Key Rules

1. **Title Numbering**: `# 1.` / `## 1.1` — file sort number independent from internal `# 1.`
2. **Cross References**: `[[file]]` or `[[file|display text]]`, no `.md` extension
3. **No Frontmatter**: no `---`, tags, aliases, or `%%` comments
4. **Code Blocks**: always annotate language
5. **Images**: `![desc](picture/file.png)`, lowercase `.png`
6. **File Naming**: `number. name.md`
7. **Bilingual Writing**: English terms, {explanatory_language} explanations
```

## CLAUDE.md Quick Reference（精简模式）

```markdown
## Quick Reference

| Item | Rule |
|------|------|
| **Code Blocks** | Fenced with language annotation |
| **Images** | `![description](path/file.png)` |
| **Note Links** | `[[file]]` or `[[file\|display text]]` |

## Getting Started

Minimal rule set. Run `/init-note-vault` in default mode to upgrade.
```

## 02-note-conventions.md 可选块

**完整性检查**：

```bash
grep -roP '\[\[[^$\][]+?\]\]' . --include='*.md' | grep -v '\.git/' | sort -u
```

**全量语言标注**：c, cpp, bash, powershell, makefile, go, python, lua, java, sql, plain

**精简语言标注**：c, cpp, bash, powershell, makefile

本 vault 权威版本见 [02-note-conventions.md](../../instructions/02-note-conventions.md)。

## Directory Structure 段落

```markdown
## Directory Structure

| Directory | Topic | Directory | Topic |
|-----------|-------|-----------|-------|
| `NN.Subject/` | Topic notes | `picture/` | Images |
| `readme/` | README files | `.claude/` | Config |
```
