# probe-toolchain.ps1 — wrapper: delegates to probe-toolchain.py (python > powershell)
param(
    [string]$VaultRoot = "",
    [switch]$JsonOnly
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $VaultRoot) {
    $VaultRoot = (Resolve-Path (Join-Path $ScriptDir "..\..\..\..")).Path
}

$PyScript = Join-Path $ScriptDir "probe-toolchain.py"
$py = $null
foreach ($name in @("python", "python3", "py")) {
    $c = Get-Command $name -ErrorAction SilentlyContinue
    if ($c) { $py = $c.Source; break }
}

if ($py -and (Test-Path $PyScript)) {
    $args = @($PyScript, "--vault-root", $VaultRoot)
    if ($JsonOnly) { $args += "--json-only" }
    & $py @args
    exit $LASTEXITCODE
}

Write-Error "probe-toolchain.ps1: Python not found. Install Python and re-run, or use Git Bash wrapper."
exit 127
