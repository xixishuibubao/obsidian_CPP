---
name: init-win-env
description: Initializes Windows terminal environment by detecting Git Bash/PowerShell paths and generating shell rules. Use when setting up a new machine, fixing terminal issues, or invoking /init-win-env.
disable-model-invocation: true
---

# /init-win-env — Windows Claude Code 环境初始化

在 Windows 上让 Claude Code 具备稳定的终端运行环境。运行时探测所有路径，不硬编码。

---

## 执行流程

### 0. 预检与冲突检测

检查 `CLAUDE.md` 是否已有 Shell 段落、`04-shell-config.md` 是否已存在；冲突时询问追加/覆盖/跳过。

### 1. 环境探测

**优先**读取 `.claude/toolchain.json`（若存在且 `generated_at` ≤ 7 天）：取 `tools.git.selected.path`、`tools.bash.selected.path` 用于验证与展示。

否则运行 `/probe-toolchain`（`python .claude/skills/probe-toolchain/scripts/probe-toolchain.py`），或最小探测：

| 探测项 | 命令 | 失败引导 |
|--------|------|----------|
| Git | `git --version` | 安装 [Git for Windows](https://git-scm.com/download/win) |
| Bash | `bash -c "echo ok"` | 检查 Git 安装目录下 `bin/bash.exe` |
| 系统语言 | `(Get-Culture).Name`（CJK 时写入 UTF-8 规则） | — |

探测失败时给出精确下载链接 + PATH 修复命令，不硬编码路径。

### 2. 生成配置

**优先**生成或更新 `.claude/instructions/04-shell-config.md`（与本 vault 权威一致）；`CLAUDE.md` 仅保留摘要：

```markdown
## Shell & Terminal

- 中文内容优先 **Git Bash**；乱码时回退 PowerShell 并设 `$env:LC_ALL = 'C.UTF-8'`
- 细则见 [04-shell-config.md](.claude/instructions/04-shell-config.md)
```

完整 Shell 策略（任务分类、Python 兜底等）仅写入 `04-shell-config.md`，勿重复膨胀 CLAUDE.md。

通用模板（非本 vault 默认）见 [reference.md](reference.md) §Shell 模板。

### 3. 生成 .claude/settings.json（通用权限预设）

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Bash(echo *)",
      "PowerShell(Get-ChildItem *)",
      "PowerShell(Select-String *)",
      "PowerShell(Get-Command *)",
      "PowerShell(Get-Content *)",
      "PowerShell(Test-Path *)",
      "PowerShell(Write-Output *)"
    ]
  }
}
```

如果已有 `.claude/settings.json`，合并追加而非覆盖。新增的权限条目包括常见的只读操作（`cat`, `ls`, `Get-Content`, `Test-Path` 等）。

### 4. 写入已知问题 MEMORY（可选）

如果系统为 CJK 环境，写入一条 memory 记录 UTF-8 编码已知问题，方便后续会话自动引用。

### 5. 验证

执行验证确认生成的规则有效：

```bash
# 验证 bash 路径是否正确
bash -c "echo ok"

# 验证 git 是否可用
git --version
```

展示给用户：

```
✓ 环境初始化完成：
  - Git Bash 路径: C:\Program Files\Git\bin\bash.exe
  - Git 版本: git version 2.45.1.windows.1
  - 系统语言: zh-CN

  - CLAUDE.md: Shell 规则段落已写入
  - .claude/settings.json: 权限已合并（含 10 条允许规则）

  Shell 验证:
    bash -c "echo ok" → ok    ✓
    git --version      → 正常  ✓

> 环境就绪。建议下一步：运行 `/probe-toolchain` 探测 Python/Node/Perl 等工具链。
```

## 使用时机

- 在新机器上首次使用 Claude Code 时
- Claude Code 终端行为异常时
- 重装 Git 或系统后

## 注意事项

- 所有路径必须运行时探测，不得硬编码默认值
- 探测失败时应给出**精确的下载链接 + 修复命令**，而非笼统的"请手动安装"
- settings.json 合并时保留用户已有配置项
- 权限预设覆盖常见的读操作（`cat`, `ls`, `Get-Content`, `Test-Path`）
- 验证步骤实际运行 bash 和 git 确认生成规则可用
- 写入 memory 时仅限 CJK 环境，避免冗余

## 相关文件

- [04-shell-config.md](../../instructions/04-shell-config.md)
- [../probe-toolchain/SKILL.md](../probe-toolchain/SKILL.md)
- [../init-git-convention/SKILL.md](../init-git-convention/SKILL.md)
- [../init-note-vault/SKILL.md](../init-note-vault/SKILL.md)

**Bootstrap 顺序**：`init-win-env` → `probe-toolchain` → `init-git-convention` → `init-note-vault`

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)
