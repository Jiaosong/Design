$ErrorActionPreference = "Stop"

$tunnelClient = "D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe"
if (-not (Test-Path -LiteralPath $tunnelClient)) {
    throw "OpenAI tunnel-client is not installed at the verified runtime path. Follow OPENAI_TUNNEL.md."
}

$tunnelId = $env:CONTROL_PLANE_TUNNEL_ID
if (-not $tunnelId) {
    throw "CONTROL_PLANE_TUNNEL_ID is not set. Create/select a tunnel in OpenAI Platform first."
}
if ($tunnelId -notmatch '^tunnel_[A-Za-z0-9]+$') {
    throw "CONTROL_PLANE_TUNNEL_ID does not look like a tunnel_* identifier."
}

& $tunnelClient init `
    --sample sample_mcp_remote_no_auth `
    --profile oleander-baidu `
    --tunnel-id $tunnelId `
    --mcp-server-url "http://127.0.0.1:8000/mcp"

if ($LASTEXITCODE -ne 0) {
    throw "tunnel-client init failed with exit code $LASTEXITCODE"
}

Write-Host "Profile 'oleander-baidu' initialized."
Write-Host "Next: set CONTROL_PLANE_API_KEY, run doctor --explain, then run the tunnel."
