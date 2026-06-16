# Shell 与终端配置

## 首选终端

优先使用 **Git Bash**（Git for Windows 自带的 Bash）执行命令。通常位于：

- `C:\Program Files\Git\bin\bash.exe`
- `C:\Program Files\Git\git-bash.exe`

## 回退策略

以下情况回退到 **PowerShell**（powershell.exe）：

1. Git Bash 不可用（未安装或 PATH 未配置）
2. Git Bash 输出乱码，尤其是中文内容显示为问号乱码
3. 需要执行 PowerShell 特有的 cmdlet（如 Get-ChildItem、Select-Object）

## 编码处理

处理中文内容时，设置 UTF-8 环境变量以避免乱码：

```bash
export LC_ALL=C.UTF-8
export LC_ALL=en_US.UTF-8
```

在 PowerShell 中等效：

```powershell
$env:LC_ALL = 'C.UTF-8'
```

### 已知问题

- PowerShell 的 git log 在中文 Windows 下显示中文为乱码
- 实际 Git 数据是 UTF-8 编码，可用 git cat-file -p 验证
- 查看 log 时可用编辑器打开解决终端乱码

## Git 路径约定

Git for Windows 使用 msys2 路径格式：
- `C:\Users\<用户名>\` 对应 `/c/Users/<用户名>/`
- 传递给 git filter-branch 的 msg-filter 等参数需要此格式
