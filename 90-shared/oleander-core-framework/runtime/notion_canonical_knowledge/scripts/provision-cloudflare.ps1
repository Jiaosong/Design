param(
  [switch]$Apply
)

$ErrorActionPreference = "Stop"
$commands = @(
  "npx wrangler d1 create oleander-knowledge-manifest --location=apac",
  "npx wrangler queues create oleander-notion-ingest",
  "npx wrangler queues create oleander-notion-ingest-dlq",
  "npx wrangler vectorize create oleander-knowledge-v1 --dimensions=1024 --metric=cosine"
)

Write-Host "OLEANDER Notion Canonical Knowledge provisioning plan"
Write-Host "This script creates Cloudflare account resources. It does not run unless -Apply is supplied."
Write-Host ""
$commands | ForEach-Object { Write-Host "  $_" }

if (-not $Apply) {
  Write-Host ""
  Write-Host "Dry run only. Re-run with -Apply after reviewing account/cost implications."
  exit 0
}

foreach ($command in $commands) {
  Write-Host ""
  Write-Host "> $command"
  Invoke-Expression $command
}

Write-Host ""
Write-Host "Next: copy the D1 database_id into wrangler.jsonc, then run migrations and set secrets:"
Write-Host "  npx wrangler d1 migrations apply oleander-knowledge-manifest --remote"
Write-Host "  npx wrangler secret put NOTION_TOKEN"
Write-Host "  npx wrangler secret put NOTION_WEBHOOK_VERIFICATION_TOKEN"
Write-Host "  npx wrangler secret put OLEANDER_API_TOKEN"
