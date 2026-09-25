$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$secretFile = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets\baidu-netdisk-access-token.dpapi"
$localPort = 9823

if (-not (Test-Path -LiteralPath $secretFile)) {
    throw "Encrypted Baidu token not found. Run configure_baidu_token.ps1 first."
}

$encrypted = (Get-Content -LiteralPath $secretFile -Raw).Trim()
$secure = ConvertTo-SecureString $encrypted
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
    $env:BAIDU_NETDISK_ACCESS_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

$existing = Get-NetTCPConnection -LocalPort $localPort -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    try {
        $health = Invoke-RestMethod "http://127.0.0.1:$localPort/healthz" -TimeoutSec 3
        if ($health.status -eq "ok" -and $health.token_configured -eq $true) {
            Write-Host "OLEANDER Baidu Storage is already running on 127.0.0.1:$localPort." -ForegroundColor Green
            Remove-Item Env:BAIDU_NETDISK_ACCESS_TOKEN -ErrorAction SilentlyContinue
            exit 0
        }
    } catch {}
    Remove-Item Env:BAIDU_NETDISK_ACCESS_TOKEN -ErrorAction SilentlyContinue
    throw "Port $localPort is already in use by another process. Stop that process before starting OLEANDER Baidu Storage."
}

Set-Location $here
try {
    $env:PORT = [string]$localPort
    $env:OLEANDER_TRUST_PRIVATE_TRANSPORT = "true"
    $env:PYTHONUTF8 = "1"
    Write-Host "Starting OLEANDER Baidu Storage on http://127.0.0.1:$localPort/mcp" -ForegroundColor Cyan
    py -3.13 -m app.server
} finally {
    Remove-Item Env:BAIDU_NETDISK_ACCESS_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:PORT -ErrorAction SilentlyContinue
    Remove-Item Env:OLEANDER_TRUST_PRIVATE_TRANSPORT -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
}
