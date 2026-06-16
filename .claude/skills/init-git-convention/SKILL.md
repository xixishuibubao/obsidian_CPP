---
name: init-git-convention
description: 为任意项目注入 Conventional Commits 工作流规范 — 生成 CLAUDE.md、子指令文件及权限预设
---

# /init-git-convention — Git 工作流规范初始化

为任意项目（不限语言）注入 Conventional Commits + 整洁 Git 工作流规范。

---

## 执行流程

### 0. 预检

```bash
git --version                     # 检查 git 是否可用
git rev-parse --git-dir 2>NUL     # 检查当前目录是否在 git 仓库内
```

| 检查项 | 通过 | 失败处理 |
|--------|------|----------|
| git 已安装 | 继续 | 提示"git 未安装或不在 PATH 中，请先安装 https://git-scm.com/downloads"，退出 |
| 在 git 仓库内 | 继续 | 提示"当前目录不是 git 仓库，请先 `git init` 或在仓库目录下运行"，退出 |

### 1. 询问语言偏好 & 项目类型

```
? Commit 描述使用哪种语言？
   ──
   [✓] 中文（推荐：描述更精确，适合个人/中文团队项目）
   [ ] English (recommended for open-source/international projects)
   ──
```

```
? 项目类型是什么？（影响 scope 约定和示例）
   ──
   [✓] 个人笔记/知识库（推荐 scope: 目录名，如 docs(linux)）
   [ ] 开源库/框架（推荐 scope: 模块/组件名，如 feat(core)）
   [ ] 企业内部项目（推荐 scope: 服务/领域名，如 fix(payment)）
   ──
```

默认选中中文 + 个人笔记/知识库。

### 2. 生成 CLAUDE.md（Git 工作流段落）

```markdown
## Git Workflow

- **Commit after each change**: After each modification, commit locally with a proper Conventional Commits message.
- **Squash before remote push**: Before pushing to remote, squash/fixup accumulated local commits into clean commits. Keep remote log concise and meaningful.
- **Commit message format**: Must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <{language_description}>
```

### Common Types

| Type       | Usage                       |
|------------|-----------------------------|
| `feat`     | New feature / content       |
| `fix`      | Bug fix                     |
| `docs`     | Documentation               |
| `style`    | Formatting, whitespace      |
| `refactor` | Restructure, no behavior change |
| `perf`     | Performance improvement     |
| `test`     | Testing                     |
| `chore`    | Tooling, config, deps       |
| `ci`       | CI configuration            |
| `build`    | Build system                |

### Scope Convention

{scope_example}
```

`{language_description}` 和 `{scope_example}` 占位符替换规则：

| 偏好 | `{language_description}` | `{scope_example}` |
|------|-------------------------|-------------------|
| 中文 + 个人笔记 | `"描述"` | Use directory name or topic name, e.g., `docs(linux)`, `fix(c-lang)` |
| 中文 + 开源库 | `"描述"` | Use module/component name, e.g., `feat(core)`, `fix(parser)` |
| 中文 + 企业项目 | `"描述"` | Use service/domain name, e.g., `feat(payment)`, `fix(auth)` |
| English + 任意 | `"description"` | 对应英文版的 scope 示例 |

### 3. 生成 .claude/instructions/01-git-workflow.md

```markdown
# Git Workflow Reference

## Local Commit Flow

1. Commit after each change:
   ```bash
   git commit -m "type(scope): {description}"
   ```
2. Keep each commit focused on a single change.
3. {description_language_rule}

## Squash Before Push

### Method A: git reset --soft (Simple)

```bash
git reset --soft HEAD~N
git commit -m "type(scope): Complete description"
```

Use when you have N trivial micro-commits that should be one.

### Method B: GIT_SEQUENCE_EDITOR (Automated)

```bash
# 自动将指定提交标记为 fixup
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \(sha\|sha\)/fixup \1/'" git rebase -i HEAD~N
```

Use when commits have meaningful individual messages worth keeping.

### Handling Auto-Backup Commits

Some tools (e.g., obsidian-git) generate automated backup commits with patterns like `vault backup: YYYY-MM-DD HH:MM:SS`. These can be automatically detected and fixup'd using Method B.

## .gitignore Template

```
# OS
.DS_Store
Thumbs.db

# Editor
*.swp
*.swo
*~
.vscode/
.idea/

# Build / Dependencies (language-agnostic common)
*.o
*.a
*.so
*.dylib
*.exe
*.dll
*.lib
*.class
*.pyc
node_modules/
vendor/
target/

# Large binary
*.mp4
*.pdf
*.zip
*.tar.gz
```

## Empty Directory Tracking

Use `.gitkeep` to track empty directories:
- Empty dir → `.gitkeep` file
- Dir has content → remove redundant `.gitkeep`
```

### 4. 合并权限

读取并更新 `.claude/settings.json`：

```powershell
# 读取现有配置
$settings = @{}
if (Test-Path ".claude/settings.json") {
    $settings = Get-Content ".claude/settings.json" -Raw | ConvertFrom-Json
}

# 注入 git 权限（如果已有则跳过重复项）
$gitPermissions = @(
    "Bash(git add *)",
    "Bash(git commit -m *)",
    "Bash(git reset --soft *)",
    "Bash(git rebase *)",
    "Bash(git log *)",
    "Bash(git status *)",
    "Bash(git diff *)"
)

if (-not $settings.permissions) { $settings.permissions = @{} }
if (-not $settings.permissions.allow) { $settings.permissions.allow = @() }

$existing = $settings.permissions.allow
$gitPermissions | % { if ($_ -notin $existing) { $existing += $_ } }

# 写回（保持格式整洁）
$settings | ConvertTo-Json -Depth 4 | Set-Content ".claude/settings.json" -Encoding utf8
```

如果已有 `.claude/settings.json`，追加不重复的权限条目；不存在则创建。

### 5. 生成 CLAUDE.md 自管理段落

```markdown
## CLAUDE.md Self-Management

- Keep root CLAUDE.md concise: Root CLAUDE.md should stay under 150–180 lines. When it grows beyond, split detailed content into `.claude/instructions/` sub-files.
- Sub-file convention: Place detailed instructions in `.claude/instructions/01-*.md`, `02-*.md`, etc.
- Reference from root: Root CLAUDE.md should only contain essential rules and links to sub-files.
```

### 6. 验证

```bash
# 检查生成的指令文件是否存在
ls .claude/instructions/ 2>/dev/null || echo "No .claude/instructions/ directory"
```

展示给用户：

```
✓ 初始化完成：
  - CLAUDE.md: Git 工作流段落已写入
  - .claude/instructions/01-git-workflow.md: 已创建
  - .claude/settings.json: Git 权限已合并

  建议下一步：检查 CLAUDE.md 确保无冲突，然后提交初始化：
    git add -A && git commit -m "chore(claude): 初始化 Git 工作流规范"
```

## 使用时机

- 初始化任意新项目时
- 为没有 Git 规范的老项目追加规范

## 注意事项

- **必须预检**：git 是否安装、当前目录是否在仓库内
- 如项目已有 `.claude/instructions/` 目录，使用下一个可用编号（例如已有 `01-`，则创建 `02-git-workflow.md`）
- 如项目 CLAUDE.md 已有 Git 段落，询问用户是否覆盖或合并
- scope 约定根据项目类型调整，不绑定特定语言
- settings.json 合并时使用完整的 PowerShell 命令而非模糊描述
