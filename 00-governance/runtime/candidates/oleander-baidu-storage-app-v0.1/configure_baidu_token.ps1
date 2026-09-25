$ErrorActionPreference = "Stop"

$authUrl = "https://openapi.baidu.com/oauth/2.0/authorize?response_type=token&client_id=QHOuRXiepJBMjtk0esLhrPoNlQyYd0mF&redirect_uri=oob&scope=basic,netdisk"
$secretDir = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets"
$secretFile = Join-Path $secretDir "baidu-netdisk-access-token.dpapi"

Write-Host "Opening the official Baidu Netdisk MCP personal-test authorization URL..."
Write-Warning "The official Baidu repository states that personal-user credentials are for limited-time testing and may change."
Start-Process $authUrl

Write-Host "After authorizing, you may paste either:"
Write-Host "  1) only the access_token value; or"
Write-Host "  2) the full callback URL / copied text containing access_token=."
$secureInput = Read-Host "Paste token or full authorization result (input will be hidden)" -AsSecureString
if ($secureInput.Length -lt 10) {
    throw "Authorization result looks empty or too short. Nothing was saved."
}

$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureInput)
try {
    $raw = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

try {
    $token = $null
    if ($raw -match '(?:^|[#?&\s])access_token=([^&\s#]+)') {
        $token = [Uri]::UnescapeDataString($Matches[1])
    } elseif ($raw -notmatch '[\s:/?&#=]') {
        $token = $raw.Trim()
    }

    if ([string]::IsNullOrWhiteSpace($token) -or $token.Length -lt 10) {
        throw "Could not extract a valid access_token. Paste the full callback URL or only the token value. Nothing was saved."
    }

    $secureToken = ConvertTo-SecureString -String $token -AsPlainText -Force
} finally {
    $raw = $null
    $token = $null
}

New-Item -ItemType Directory -Force -Path $secretDir | Out-Null
$encrypted = ConvertFrom-SecureString -SecureString $secureToken
Set-Content -LiteralPath $secretFile -Value $encrypted -Encoding UTF8

Write-Host "Saved an encrypted current-user DPAPI token at: $secretFile"
Write-Host "The plaintext token was not written to the repository."
