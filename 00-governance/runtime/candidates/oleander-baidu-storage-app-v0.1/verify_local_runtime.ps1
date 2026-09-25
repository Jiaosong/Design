$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$codex = "C:\Users\Xianmu\AppData\Local\OpenAI\Codex\bin\13995fba801849b0\codex.exe"
$pluginId = "oleander-baidu-storage@oleander-personal"
$cacheRoot = Join-Path $env:USERPROFILE ".codex\plugins\cache\oleander-personal\oleander-baidu-storage"
$secretFile = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets\baidu-netdisk-access-token.dpapi"

if (-not (Test-Path -LiteralPath $codex)) {
    throw "Codex CLI not found at the verified workstation path."
}
if (-not (Test-Path -LiteralPath $secretFile)) {
    throw "Baidu DPAPI token is missing. Run configure_baidu_token.ps1 first."
}

$installedJson = & $codex plugin list --json
if ($LASTEXITCODE -ne 0) { throw "codex plugin list failed" }
$installed = ($installedJson | ConvertFrom-Json).installed | Where-Object { $_.pluginId -eq $pluginId }
if (-not $installed -or -not $installed.enabled) {
    throw "$pluginId is not installed and enabled."
}

$version = [string]$installed.version
$wrapper = Join-Path $cacheRoot "$version\runtime\run_stdio_secure.ps1"
if (-not (Test-Path -LiteralPath $wrapper)) {
    throw "Installed stdio wrapper is missing: $wrapper"
}

$mcp = & $codex mcp get oleander_baidu_storage --json
if ($LASTEXITCODE -ne 0) { throw "Codex does not resolve oleander_baidu_storage." }
$mcpConfig = $mcp | ConvertFrom-Json
if (-not $mcpConfig.enabled -or $mcpConfig.transport.type -ne "stdio") {
    throw "oleander_baidu_storage is not enabled as stdio in Codex."
}

Write-Host "Codex plugin: $pluginId $version (enabled)" -ForegroundColor Green
Write-Host "Codex MCP: oleander_baidu_storage (stdio enabled)" -ForegroundColor Green

py -3.13 (Join-Path $here "scripts\verify_installed_local_runtime.py") $wrapper
if ($LASTEXITCODE -ne 0) {
    throw "Installed OLEANDER Baidu Storage runtime verification failed."
}

Write-Host "PASS_LOCAL_COS_CODEX_BAIDU_STORAGE" -ForegroundColor Green
