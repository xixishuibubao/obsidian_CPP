---
name: init-note-vault
description: 为 Obsidian / Markdown 知识库初始化笔记规范 — 支持默认模式（完整规则）与精简模式（最小规则集）
---

# /init-note-vault — 笔记知识库规范初始化

为 Obsidian 或 Markdown 知识库仓库初始化笔记内容规范。

---

## 执行流程

### 0. 预检与冲突检测

```bash
ls CLAUDE.md 2>/dev/null || echo "not found"
```

检查项：

| 检查 | 通过 | 冲突处理 |
|------|------|----------|
| CLAUDE.md 是否存在 | 读取内容，检查是否有已有规范 | 不存在 → 新建；存在 → 检查是否已有 Notes 相关段落 |
| 是否已有 `.claude/instructions/` | 确认是否已存在编号体系 | 存在 → 追加时用下一个编号 |
| 是否已有 `02-note-conventions.md` | 读取内容避免重复注入 | 存在 → 询问「追加/覆盖/跳过」 |

如果检测到已有规范段落，询问用户：

```
检测到 CLAUDE.md 中已有笔记规范相关内容:
  - 已有「Quick Reference」表格
  - 已有「Key Rules」段落

? 如何处理已有规范？
   ──
   [✓] 追加 — 合并已有 + 新增规则，不删除任何内容
   [ ] 覆盖 — 用本次生成的规范完全替换
   [ ] 跳过 — 保持现有规范不变
   ──
```

### 1. 询问使用模式

```
? 选择笔记规范模式：
   ──
   [✓] 默认模式 — 包含完整规则集（标题编号、wikilink、无 frontmatter、代码块标注、双语写作...）
   [ ] 精简模式 — 仅包含最小通用规则集，提示用户可自行扩展
   ──
```

默认选中默认模式。

### 2. 询问模板参数

```
? 请选择以下模板项（多选）:
   ──
   [✓] 完整性检查命令 — 生成检查 wikilink 断链/标题格式的 bash 命令
   [✓] 全量语言标注列表 — c/cpp/bash/powershell/makefile/go/python/lua/java/sql/plain
   [ ] 精简语言标注列表 — 仅 c/cpp/bash/powershell/makefile
   [✓] .gitkeep 维护脚本段落 — 生成维护空目录占位的命令
   ──
```

### 3. 生成 CLAUDE.md（Quick Reference 表格 + Key Rules）

**默认模式**输出：

```markdown
## Quick Reference

| Item | Rule |
|------|------|
| **Note Links** | Obsidian wikilink `[[file\|display text]]`；表格内禁止 `\|` 别名（见 conventions） |
| **Title Format** | `# 1.`, `## 1.1`, `### 1.1.1` numbered |
| **Frontmatter** | No YAML frontmatter or tags |
| **Code Blocks** | Fenced with language annotation (c, cpp, bash, python, go, sql, ...) |
| **Images** | `![description](picture/filename.png)` |
| **Style** | Bilingual writing: English terms, {explanatory_language} explanation |
| **Empty Dirs** | `.gitkeep` placeholder files |

## Key Rules

1. **Title Numbering**: `# 1.` / `## 1.1` / `### 1.1.1` — no `**` bold in titles, no manual Chinese numbering (一、二、三). File name sort number (e.g., `5. Note.md`) is independent from internal title number (always starts from `# 1.`)
2. **Cross References**: Use `[[file]]` or `[[file|display text]]`, no `.md` extension in link target
3. **No Frontmatter**: Do not use `---` metadata blocks, tags, aliases, or Obsidian `%%` comments
4. **Code Blocks**: Always annotate language — see full reference for supported languages
5. **Images**: Reference as `![desc](picture/file.png)`, consistently use lowercase `.png` even if disk is `.PNG`
6. **File Naming**: `number. name.md` — e.g., `1. C++ Basics.md`, `8. Common Commands.md`
7. **Bilingual Writing**: Technical terms in English, explanations in {explanatory_language}
```

其中 `{explanatory_language}` 根据用户偏好设定（默认为中文 `zh`）。

**精简模式**输出：

```markdown
## Quick Reference

| Item | Rule |
|------|------|
| **Code Blocks** | Fenced with language annotation |
| **Images** | `![description](path/file.png)` |
| **Note Links** | `[[file]]` or `[[file\|display text]]`（表格外）；表格内见 conventions |

## Getting Started

This is a minimal rule set. To extend with full conventions, run `/init-note-vault` again and choose **default mode**, or manually add rules to `.claude/instructions/02-note-conventions.md`.
```

### 4. 生成 .claude/instructions/02-note-conventions.md

**默认模式**：

当用户选择了「完整性检查命令」时，在文件中包含：

```markdown
## Link Integrity Check

The CLAUDE.md one-click check command may mistakenly match shell `[[ ]]` conditions (e.g., `[[ $var == x ]]`) as wikilinks. These are not real wikilinks and can be ignored.

For accurate broken link detection, use:

```bash
grep -roP '\[\[[^$\][]+?\]\]' . --include='*.md' | grep -v '\.git/' | sort -u
```

This excludes wikilinks containing `$` to filter out shell variable references, keeping only real file references.
```

当用户选择了「全量语言标注列表」：

```markdown
## Code Blocks

Fenced code blocks with language annotation:

| Language  | Tag        |
|-----------|------------|
| C         | `c`        |
| C++       | `cpp`      |
| Shell     | `bash`     |
| PowerShell| `powershell` |
| Makefile  | `makefile` |
| Go        | `go`       |
| Python    | `python`   |
| Lua       | `lua`      |
| Java      | `java`     |
| SQL       | `sql`      |
| Plain text| `plain`    |
```

当用户选择了「精简语言标注列表」：

```markdown
## Code Blocks

Fenced code blocks with language annotation (minimum set):

| Language  | Tag        |
|-----------|------------|
| C         | `c`        |
| C++       | `cpp`      |
| Shell     | `bash`     |
| PowerShell| `powershell` |
| Makefile  | `makefile` |
```

当用户选择了「.gitkeep 维护脚本段落」时，在文件中包含 `.gitkeep` 管理说明。

其余固定内容（标题编号、跨笔记引用、图片引用、无 frontmatter、文件命名等）保持不变。

**精简模式**：仅写入 Code Blocks 表格 + Images + File Naming 基础规则，末尾加上扩展提示。

### 5. 生成参考目录结构段落

写入 CLAUDE.md：

```markdown
## Directory Structure

| Directory | Topic | Directory | Topic |
|-----------|-------|-----------|-------|
| `NN.Subject/` | Topic notes | `picture/` | Images |
| `readme/` | README files | `.claude/` | Config |

_(Use descriptive numbered directory names for each subject area.)_
```

使用通用占位符，不绑定具体科目。

### 6. 验证

```bash
# 检查 Quick Reference 表格是否在 CLAUDE.md 中
grep -c "Quick Reference" CLAUDE.md 2>/dev/null || echo "not found"
# 检查 instructions 文件是否存在
ls .claude/instructions/02-note-conventions.md 2>/dev/null || echo "not found"
```

展示给用户：

```
✓ 初始化完成：
  - CLAUDE.md: Quick Reference + Key Rules 已写入
  - .claude/instructions/02-note-conventions.md: 已创建
  ──
  选择项:
    - 模式: 默认（完整规则集）
    - 语言: 中文
    - 完整性检查命令: ✓ 已启用
    - 语言标注列表: 全量 (11 种)
    - .gitkeep 维护脚本: ✓ 已启用
```

## 使用时机

- 新建 Obsidian 知识库仓库时运行
- 为已有笔记仓库追加格式规范时运行

## 注意事项

- **必须先检测冲突**：检查 CLAUDE.md 是否已有规范段落，询问用户处理方式
- 默认模式完整输出全部规则集
- 精简模式适合快速起步，用户可后续运行 `/init-note-vault` 切换到默认模式升级
- 如项目已有 CLAUDE.md，根据用户选择合并追加或覆盖
- 目录结构表使用通用描述，不绑定具体科目名称
- 模板项可配置：完整性检查、语言标注列表长度、.gitkeep 维护脚本
- **instructions 编号**：扫描 `.claude/instructions/` 取下一可用序号，勿硬编码 `02-`（本 vault 已有 `01`–`07`）
- 完成后建议运行 `/init-git-convention`（若尚无 Git 规范）

## 相关文件

- [02-note-conventions.md](../../instructions/02-note-conventions.md) — 本 vault 权威笔记规范
- [../init-git-convention/SKILL.md](../init-git-convention/SKILL.md)
- [../init-win-env/SKILL.md](../init-win-env/SKILL.md)
