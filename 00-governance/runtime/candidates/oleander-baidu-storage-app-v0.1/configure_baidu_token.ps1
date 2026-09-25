$ErrorActionPreference = "Stop"

$authUrl = "https://openapi.baidu.com/oauth/2.0/authorize?response_type=token&client_id=QHOuRXiepJBMjtk0esLhrPoNlQyYd0mF&redirect_uri=oob&scope=basic,netdisk"
$secretDir = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets"
$secretFile = Join-Path $secretDir "baidu-netdisk-access-token.dpapi"

Write-Host "Opening the official Baidu Netdisk MCP personal-test authorization URL..."
Write-Warning "The official Baidu repository states that personal-user credentials are for limited-time testing and may change."
Start-Process $authUrl

Write-Host "After authorizing, copy only the access_token value from the Baidu result page."
$secureToken = Read-Host "Paste access_token (input will be hidden)" -AsSecureString
if ($secureToken.Length -lt 10) {
    throw "Token looks empty or too short. Nothing was saved."
}

New-Item -ItemType Directory -Force -Path $secretDir | Out-Null
$encrypted = ConvertFrom-SecureString -SecureString $secureToken
Set-Content -LiteralPath $secretFile -Value $encrypted -Encoding UTF8

Write-Host "Saved an encrypted current-user DPAPI token at: $secretFile"
Write-Host "The plaintext token was not written to the repository."
