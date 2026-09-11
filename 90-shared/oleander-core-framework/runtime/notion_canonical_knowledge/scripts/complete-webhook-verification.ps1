param(
  [switch]$ClearCapturedToken
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

if ($ClearCapturedToken) {
  npx wrangler d1 execute oleander-knowledge-manifest --remote --command "DELETE FROM runtime_state WHERE state_key='pending_notion_webhook_verification_token';"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host "Captured webhook setup token state cleared from D1."
  exit 0
}

$devVars = Join-Path $root ".dev.vars"
if (-not (Test-Path -LiteralPath $devVars)) {
  throw ".dev.vars is missing; OLEANDER_API_TOKEN is required to decrypt the captured webhook verification token."
}

$apiLine = Get-Content -LiteralPath $devVars | Where-Object { $_ -match '^OLEANDER_API_TOKEN=' } | Select-Object -First 1
if (-not $apiLine) { throw "OLEANDER_API_TOKEN is missing from .dev.vars." }
$apiToken = $apiLine.Substring('OLEANDER_API_TOKEN='.Length)

$raw = npx wrangler d1 execute oleander-knowledge-manifest --remote --json --command "SELECT state_value, updated_at FROM runtime_state WHERE state_key='pending_notion_webhook_verification_token';"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$parsed = $raw | ConvertFrom-Json
$row = $parsed[0].results | Select-Object -First 1
if (-not $row) {
  throw "No captured Notion webhook verification token found yet. Create the subscription in Notion first."
}

$env:OLEANDER_SETUP_CIPHERTEXT = [string]$row.state_value
$env:OLEANDER_SETUP_KEY = $apiToken
try {
  $token = node -e @'
const crypto = require('crypto');
const value = process.env.OLEANDER_SETUP_CIPHERTEXT;
const apiToken = process.env.OLEANDER_SETUP_KEY;
const [ivPart, cipherPart] = value.split('.');
const key = crypto.createHash('sha256').update(`oleander:webhook-setup:${apiToken}`).digest();
const packed = Buffer.from(cipherPart, 'base64');
const body = packed.subarray(0, packed.length - 16);
const tag = packed.subarray(packed.length - 16);
const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(ivPart, 'base64'));
decipher.setAuthTag(tag);
process.stdout.write(Buffer.concat([decipher.update(body), decipher.final()]).toString('utf8'));
'@
} finally {
  Remove-Item Env:OLEANDER_SETUP_CIPHERTEXT -ErrorAction SilentlyContinue
  Remove-Item Env:OLEANDER_SETUP_KEY -ErrorAction SilentlyContinue
}

if (-not $token) { throw "Failed to decrypt the captured verification token." }

$token | npx wrangler secret put NOTION_WEBHOOK_VERIFICATION_TOKEN
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Set-Clipboard -Value $token
$token = $null
Write-Host "Webhook verification secret stored in Cloudflare."
Write-Host "The one-time verification token is now in the Windows clipboard."
Write-Host "Paste it into Notion -> Webhooks -> Verify, then run this script with -ClearCapturedToken."
