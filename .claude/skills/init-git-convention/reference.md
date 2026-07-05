# init-git-convention — 参考模板

## CLAUDE.md Git Workflow 段落

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

占位符替换：

| 偏好 | `{language_description}` | `{scope_example}` |
|------|-------------------------|-------------------|
| 中文 + 个人笔记 | `"描述"` | Use directory name, e.g., `docs(linux)`, `fix(c-lang)` |
| 中文 + 开源库 | `"描述"` | Use module name, e.g., `feat(core)`, `fix(parser)` |
| 中文 + 企业项目 | `"描述"` | Use service name, e.g., `feat(payment)`, `fix(auth)` |
| English | `"description"` | 对应英文 scope 示例 |

## instructions/NN-git-workflow.md

编号：扫描 `.claude/instructions/` 取下一可用序号（本 vault 为 `03-git-workflow.md`）。

Squash 方法 A/B、.gitignore、.gitkeep 完整模板见本 vault [03-git-workflow.md](../../instructions/03-git-workflow.md)。

## CLAUDE.md Self-Management 段落

```markdown
## CLAUDE.md Self-Management

- Keep root CLAUDE.md concise: under **100–130 lines** (this vault) or 150–180 lines (generic).
- Sub-files in `.claude/instructions/01-*.md`, `02-*.md`, etc.
- Root only contains essential rules and links to sub-files.
```

## settings.json 合并（PowerShell）

```powershell
$settings = @{}
if (Test-Path ".claude/settings.json") {
    $settings = Get-Content ".claude/settings.json" -Raw | ConvertFrom-Json
}
$gitPermissions = @("Bash(git *)", "PowerShell(Get-Content *)", "PowerShell(Set-Content *)", "PowerShell(ConvertFrom-Json *)")
if (-not $settings.permissions) { $settings.permissions = @{} }
if (-not $settings.permissions.allow) { $settings.permissions.allow = @() }
$existing = $settings.permissions.allow
$gitPermissions | % { if ($_ -notin $existing) { $existing += $_ } }
$settings | ConvertTo-Json -Depth 4 | Set-Content ".claude/settings.json" -Encoding utf8
```
