$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$secretFile = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets\baidu-netdisk-access-token.dpapi"

if (-not (Test-Path -LiteralPath $secretFile)) {
    throw "Encrypted Baidu token not found. Run configure_baidu_token.ps1 first."
}

$encrypted = Get-Content -LiteralPath $secretFile -Raw
$secure = ConvertTo-SecureString $encrypted
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
    $env:BAIDU_NETDISK_ACCESS_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

Set-Location $here
try {
    py -3.13 -m app.server
} finally {
    Remove-Item Env:BAIDU_NETDISK_ACCESS_TOKEN -ErrorAction SilentlyContinue
}
