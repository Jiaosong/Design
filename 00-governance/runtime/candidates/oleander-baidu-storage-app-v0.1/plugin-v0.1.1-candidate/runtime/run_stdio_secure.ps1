$ErrorActionPreference = "Stop"
$secretFile = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets\baidu-netdisk-access-token.dpapi"

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

$env:PYTHONUTF8 = "1"
Set-Location $PSScriptRoot
try {
    py -3.13 .\stdio_entry.py
} finally {
    Remove-Item Env:BAIDU_NETDISK_ACCESS_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:PYTHONUTF8 -ErrorAction SilentlyContinue
}
