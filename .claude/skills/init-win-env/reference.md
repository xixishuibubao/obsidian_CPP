# init-win-env — 参考模板

## Shell 模板

供无 `04-shell-config.md` 的新项目选用。`{detected_bash_path}`、`{user}` 替换为探测值。

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

- 根文件保持在 **100–130 行**以内（本 vault），超出则拆分到 `.claude/instructions/`
- 子文件同样控制在 200 行以内，超出则递归拆分
- 根文件通过 `- [标题](.claude/instructions/XX-name.md) — 描述` 引用所有子文件
```

CJK 语言（`zh-*`、`ja-*`、`ko-*`）才写入 UTF-8 与 Known Issues。

## settings.json 模板

见 SKILL.md §3。
