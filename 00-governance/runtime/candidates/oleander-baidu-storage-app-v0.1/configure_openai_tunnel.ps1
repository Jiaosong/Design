$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tunnelClient = "D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe"
$secretDir = Join-Path $env:LOCALAPPDATA "OLEANDER\secrets"
$runtimeKeyFile = Join-Path $secretDir "openai-tunnel-runtime-key.dpapi"
$profileDir = Join-Path $env:LOCALAPPDATA "OLEANDER\tunnel-client"
$profileName = "oleander-baidu-storage"

if (-not (Test-Path -LiteralPath $tunnelClient)) {
    throw "OpenAI tunnel-client not found at: $tunnelClient"
}

Write-Host "OpenAI Secure MCP Tunnel setup for OLEANDER Baidu Storage" -ForegroundColor Cyan
Write-Host "This keeps the Baidu MCP private on this workstation."
Write-Host ""
Write-Host "Create a tunnel in the already-open Platform Tunnels page, then paste only its tunnel_... ID below."
$tunnelId = (Read-Host "Tunnel ID").Trim()
if ($tunnelId -notmatch '^tunnel_[A-Za-z0-9_-]+$') {
    throw "Tunnel ID must start with tunnel_. Nothing was saved."
}

Write-Host "Create/copy a Runtime API key with Tunnels Read + Use."
$secureKey = Read-Host "Paste Runtime API key (input hidden)" -AsSecureString
if ($secureKey.Length -lt 20) {
    throw "Runtime API key looks empty or too short. Nothing was saved."
}

New-Item -ItemType Directory -Force -Path $secretDir | Out-Null
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null
Set-Content -LiteralPath $runtimeKeyFile -Value (ConvertFrom-SecureString -SecureString $secureKey) -Encoding UTF8

& $tunnelClient init `
    --sample sample_mcp_remote_no_auth `
    --profile $profileName `
    --profile-dir $profileDir `
    --tunnel-id $tunnelId `
    --mcp-server-url "http://127.0.0.1:9823/mcp" `
    --control-plane-api-key-ref "env:CONTROL_PLANE_API_KEY" `
    --health-listen-addr "127.0.0.1:0" `
    --force

if ($LASTEXITCODE -ne 0) {
    throw "tunnel-client profile creation failed."
}

Write-Host ""
Write-Host "Saved OpenAI runtime key with Windows DPAPI at:" -ForegroundColor Green
Write-Host $runtimeKeyFile
Write-Host "Created tunnel profile:" -ForegroundColor Green
Write-Host (Join-Path $profileDir ($profileName + ".yaml"))
Write-Host "No OpenAI or Baidu plaintext credential was written to the repository."

