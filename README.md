文章使用markdown书写
不同软件对markdown的格式支持不同，使用下面网址转化。飞书选公众号格式
https://markdown.lovejade.cn/

git本身不支持空文件夹追踪，需要手动添加hook。
```powershell
# pre-commit.ps1：自动生成/删除 .gitkeep（无语法错误+无乱码）

Set-StrictMode -Version Latest

$ErrorActionPreference = "Stop"

  

# 1. 切换到仓库根目录

try {

  $repoRoot = git rev-parse --show-toplevel 2>&1

  Set-Location $repoRoot

  Write-Host "🔍 已切换到仓库根目录：$repoRoot"

}

catch {

  Write-Host "❌ 无法获取仓库根目录，请在 Git 仓库内执行" -ForegroundColor Red

  exit 1

}

  

# 辅助函数：统计文件夹内“非 .gitkeep”的文件数量

function Get-NonGitkeepCount {

  param([string]$FolderPath)

  $fileCount = (Get-ChildItem -Path $FolderPath -File -ErrorAction SilentlyContinue |

                Where-Object { $_.Name -ne ".gitkeep" } |

                Measure-Object).Count

  return $fileCount

}

  

# 2. 批量给空文件夹生成 .gitkeep（排除 .git、node_modules、venv）

Write-Host ([Environment]::NewLine + "📂 正在处理空文件夹...")

Get-ChildItem -Directory -Recurse | Where-Object {

  $_.FullName -notlike "*\.git\*" -and

  $_.FullName -notlike "*node_modules*" -and

  $_.FullName -notlike "*venv*"

} | ForEach-Object {

  $folderPath = $_.FullName

  $gitkeepPath = Join-Path $folderPath ".gitkeep"

  $nonGitkeepCount = Get-NonGitkeepCount -FolderPath $folderPath

  if (($nonGitkeepCount -eq 0) -and (-not (Test-Path $gitkeepPath))) {

    New-Item -Path $gitkeepPath -ItemType File -Force | Out-Null

    # 关键：生成后立即设置为隐藏文件（Windows 原生隐藏属性）

    Set-ItemProperty -Path $gitkeepPath -Name Attributes -Value Hidden -ErrorAction SilentlyContinue

    Write-Host "✅ 生成隐藏 .gitkeep：$folderPath（文件夹为空，需追踪）"

  }

}

  

# 3. 批量删除冗余 .gitkeep（仅当文件夹内有其他文件时）

Get-ChildItem -Directory -Recurse | Where-Object {

  $_.FullName -notlike "*\.git\*" -and

  $_.FullName -notlike "*node_modules*" -and

  $_.FullName -notlike "*venv*"

} | ForEach-Object {

  $folderPath = $_.FullName

  $gitkeepPath = Join-Path $folderPath ".gitkeep"

  $nonGitkeepCount = Get-NonGitkeepCount -FolderPath $folderPath

  if ((Test-Path $gitkeepPath) -and ($nonGitkeepCount -gt 0)) {

    Remove-Item -Path $gitkeepPath -Force | Out-Null

    Write-Host "❌ 自动删除冗余 .gitkeep：$folderPath（文件夹内有其他文件）"

  }

}

  

# 4. 暂存所有 .gitkeep 变更

Write-Host ([Environment]::NewLine + "📌 正在暂存 .gitkeep 变更...")

git add ./**/.gitkeep 2>$null

  

# 完成提示（无中文乱码）

Write-Host ([Environment]::NewLine + "✅ .gitkeep 处理完成！") -ForegroundColor Green

exit 0
```

---
```bash
#!/bin/sh
# 1. 获取当前仓库根目录（绝对路径），存入变量 repo_root
repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
# 2. 脚本在仓库内的相对路径（根据实际存放位置修改！）
script_rel_path=".git/hooks/auto-gitkeep.ps1"
# 3. 拼接绝对路径（兼容 Windows 路径格式）
script_abs_path="$repo_root/$script_rel_path"
# 4. 替换路径中的 "/" 为 "\"（Windows 兼容）
script_abs_path=$(echo "$script_abs_path" | sed 's/\//\\/g')
# 5. 调用脚本（用相对路径拼接的绝对路径，无硬编码）
cmd //c powershell.exe -ExecutionPolicy Bypass -File "$script_abs_path"
exit 0
```


obsidian的git插件设置中Custom Git binary path指的是git.exe路径不是git-bash路径。