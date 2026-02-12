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
    Write-Host "✅ 生成 .gitkeep：$folderPath（文件夹为空，需追踪）"
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