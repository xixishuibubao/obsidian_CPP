---
name: init-win-env
description: Windows 环境初始化 — 探测本机 Git Bash/PowerShell 路径，生成 Shell 终端规则与权限预设
---

# /init-win-env — Windows Claude Code 环境初始化

在 Windows 上让 Claude Code 具备稳定的终端运行环境。运行时探测所有路径，不硬编码。

---

## 执行流程

### 1. 环境探测

依次执行以下探测命令（按优先级，成功后跳过后续）：

| 探测项 | 命令 | 回退策略 | 失败引导 |
|--------|------|----------|----------|
| Git Bash 路径 | `where bash` / `(Get-Command bash -ErrorAction SilentlyContinue).Source` | 检查 `$env:ProgramFiles\Git\bin\bash.exe`、`"$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"` | 引导: "未找到 Git Bash。请从 https://git-scm.com/download/win 下载安装，安装时勾选 'Git Bash Here' 选项" |
| Git 路径 | `where git` / `(Get-Command git -ErrorAction SilentlyContinue).Source` | 检查 `$env:ProgramFiles\Git\cmd\git.exe` | 引导: "未找到 git。请检查是否已安装 Git for Windows: https://git-scm.com/download/win。如已安装，可能是 PATH 未配置，请手动添加: `$env:Path += ';C:\Program Files\Git\cmd'`" |
| 系统语言 | `(Get-Culture).Name` | — | — |
| Shell 可用性 | 尝试执行 `bash -c "echo ok"` 看是否返回 `ok` 且无乱码 | — | 失败: "bash 路径可用但执行返回异常，请检查是否有安全软件拦截" |

### 2. 生成 CLAUDE.md（Shell 规则段落 + 自身管理规则）

写入以下内容（使用探测到的实际路径），追加到已有 CLAUDE.md 末尾或新建文件：

```markdown
## Shell & Terminal

- **通用原则**: 优先使用当前会话已激活的终端环境，避免环境切换开销

- **搜索/过滤类任务**（日志分析、文件内容查找、正则匹配）:
  - Unix-like 环境：`bash` + `grep`/`sed`/`awk`
  - Windows 环境：`PowerShell` + `Select-String`（性能相当）

- **文件系统操作**（遍历、状态查询、批量移动）:
  - 使用 Shell 内置命令而非外部程序（如 `**/*.log` 通配符替代 `find`）
  - 涉及大量文件（千级以上）时优先 `find -exec` 而非管道

- **复杂逻辑/API 调用/JSON 处理**:
  - 超过 3 层管道、需浮点运算、数组操作、JSON 处理时，优先 Python/Node.js 脚本
  - 避免 shell 字符串拼接的脆弱性

- **性能可观测性**: 预期超 3 秒的操作，执行前输出 `[Using: bash/zsh/pwsh/python]`

- **回退机制**: 首选终端失败且含 `syntax error` / `command not found` 时，自动降级 `bash -c "..."`，再失败则 Python 兜底

- **UTF-8 编码**: 处理中文等内容时设置 `LC_ALL=C.UTF-8` 或 `LC_ALL=en_US.UTF-8` 避免 git 输出乱码

### Known Issues

- Git Bash 路径: `{detected_bash_path}`
- PowerShell 的 `git log` 在中文 Windows 上可能乱码，可用 `git cat-file -p` 或编辑器验证
- Git for Windows 使用 msys2 路径格式: `C:\Users\{user}\` 对应 `/c/Users/{user}/`

## CLAUDE.md 自身管理

- 根文件保持在 150–180 行以内，超出则拆分到 `.claude/instructions/` 下
- 子文件同样控制在 200 行以内，超出则递归拆分（如 `01-linux-env.md` → `01-linux-env-basics.md` + `01-linux-env-advanced.md`）
- 根文件通过 `- [标题](.claude/instructions/XX-name.md) — 描述` 引用所有子文件
- 生成此规则的脚本见 `init-win-env` skill，重建规则可重新执行该 skill
```

其中 `{detected_bash_path}` 和 `{user}` 用探测到的实际值替换。

仅当系统语言为 `zh-*`、`ja-*`、`ko-*` 等 CJK 语言时写入 UTF-8 编码处理规则和 Known Issues。非 CJK 语言机器只写入 Shell 终端选择策略。

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
