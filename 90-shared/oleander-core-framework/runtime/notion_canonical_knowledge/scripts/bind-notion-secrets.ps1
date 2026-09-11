param(
  [switch]$Deploy
)

$ErrorActionPreference = "Stop"

Write-Host "OLEANDER Notion Canonical Knowledge - Notion secret binding"
Write-Host ""
Write-Host "This script intentionally uses Wrangler's interactive secret prompt."
Write-Host "The Notion token is not written to Git or echoed by this script."
Write-Host ""

npx wrangler secret put NOTION_TOKEN
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($Deploy) {
  npx wrangler deploy
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host ""
Write-Host "Notion API secret is bound."
Write-Host "Next create a Notion connection webhook subscription with:"
Write-Host "  URL: https://oleander-notion-canonical-knowledge.oleander-design-runtime.workers.dev/webhooks/notion"
Write-Host "  API version: 2026-03-11"
Write-Host ""
Write-Host "After Notion sends the one-time verification token, retrieve it through the"
Write-Host "bearer-protected /v1/webhook-setup-token endpoint, verify the subscription,"
Write-Host "store it with 'npx wrangler secret put NOTION_WEBHOOK_VERIFICATION_TOKEN',"
Write-Host "then DELETE the setup-token endpoint state."

