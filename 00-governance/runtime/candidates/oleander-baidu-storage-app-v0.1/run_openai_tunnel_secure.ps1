$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tunnelClient = "D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe"
$profileDir = Join-Path $env:LOCALAPPDATA "OLEANDER\tunnel-client"
$profileName = "oleander-baidu-storage"
$runtimeKeyFile = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets\openai-tunnel-runtime-key.dpapi"
$baiduServerScript = Join-Path $here "run_local_secure.ps1"

if (-not (Test-Path -LiteralPath $runtimeKeyFile)) {
    throw "OpenAI tunnel runtime key not configured. Run configure_openai_tunnel.ps1 first."
}
if (-not (Test-Path -LiteralPath $baiduServerScript)) {
    throw "Local Baidu MCP launcher is missing: $baiduServerScript"
}

function Get-DpapiPlaintext([string]$Path) {
    $encrypted = (Get-Content -LiteralPath $Path -Raw).Trim()
    $secure = ConvertTo-SecureString $encrypted
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

$existing = Get-NetTCPConnection -LocalPort 9823 -State Listen -ErrorAction SilentlyContinue
if (-not $existing) {
    $oldPort = $env:PORT
    $oldPrivate = $env:OLEANDER_TRUST_PRIVATE_TRANSPORT
    try {
        $env:PORT = "9823"
        $env:OLEANDER_TRUST_PRIVATE_TRANSPORT = "true"
        Start-Process powershell.exe -ArgumentList '-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + $baiduServerScript + '"') -WindowStyle Hidden | Out-Null
    } finally {
        if ($null -eq $oldPort) { Remove-Item Env:PORT -ErrorAction SilentlyContinue } else { $env:PORT = $oldPort }
        if ($null -eq $oldPrivate) { Remove-Item Env:OLEANDER_TRUST_PRIVATE_TRANSPORT -ErrorAction SilentlyContinue } else { $env:OLEANDER_TRUST_PRIVATE_TRANSPORT = $oldPrivate }
    }

    $deadline = (Get-Date).AddSeconds(20)
    do {
        Start-Sleep -Milliseconds 500
        try {
            $health = Invoke-RestMethod 'http://127.0.0.1:9823/healthz' -TimeoutSec 2
            if ($health.status -eq 'ok' -and $health.token_configured -eq $true) { break }
        } catch {}
    } while ((Get-Date) -lt $deadline)

    if ((Get-Date) -ge $deadline) {
        throw "Local Baidu MCP did not become healthy on 127.0.0.1:9823."
    }
}

$env:CONTROL_PLANE_API_KEY = Get-DpapiPlaintext $runtimeKeyFile
try {
    & $tunnelClient doctor --profile $profileName --profile-dir $profileDir --explain
    if ($LASTEXITCODE -ne 0) {
        throw "OpenAI tunnel doctor failed."
    }

    & $tunnelClient run --profile $profileName --profile-dir $profileDir
} finally {
    Remove-Item Env:CONTROL_PLANE_API_KEY -ErrorAction SilentlyContinue
}

