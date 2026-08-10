param(
  [string]$RuntimeRoot = "$PSScriptRoot\.."
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$Message) {
  Write-Host "[OLEANDER-RHINO] $Message"
}

$runtimeRootResolved = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$rhinoCode = Join-Path $env:ProgramFiles 'Rhino 8\System\rhinocode.exe'
$probe = Join-Path $runtimeRootResolved 'rhino\probe_runtime.py'
$outDir = Join-Path $runtimeRootResolved 'runtime-state'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

if (-not (Test-Path $rhinoCode)) {
  throw "rhinocode not found at $rhinoCode"
}
if (-not (Test-Path $probe)) {
  throw "Probe script not found at $probe"
}

$instancesRaw = & $rhinoCode list --json
if ($LASTEXITCODE -ne 0 -or -not $instancesRaw) {
  throw 'rhinocode cannot list a live Rhino script-server instance. Run bootstrap_windows.ps1 first.'
}

try { $instances = @($instancesRaw | ConvertFrom-Json) } catch { throw "Unable to parse rhinocode list --json: $($_.Exception.Message)" }
if ($instances.Count -eq 0) {
  throw 'No live Rhino script-server instance found.'
}

$env:OLEANDER_RHINO_OUT = $outDir
Write-Step "Running real Rhino runtime probe inside process $($instances[0].processId)..."

& $rhinoCode --rhino $instances[0].pipeId script $probe
if ($LASTEXITCODE -ne 0) {
  throw "rhinocode probe returned exit code $LASTEXITCODE"
}

$manifestPath = Join-Path $outDir 'runtime_probe_manifest.json'
if (-not (Test-Path $manifestPath)) {
  throw "Expected runtime manifest not produced: $manifestPath"
}

$manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json
Write-Step "Runtime status: $($manifest.status)"

if ($manifest.status -ne 'RHINO RUNTIME PASS / GRASSHOPPER SDK PASS') {
  throw "Runtime healthcheck did not pass. Inspect $manifestPath"
}

Write-Step 'HEALTHCHECK PASS — Rhino and Grasshopper SDK are executing in a live Rhino process.'
Write-Step 'CP2 / CP4 are still OPEN until the target definition is run and evidence is captured.'
