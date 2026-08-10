param(
  [Parameter(Mandatory=$true)][string]$JobSpec,
  [string]$PipeId = ""
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$Message) {
  Write-Host "[OLEANDER-RHINO] $Message"
}

$runtimeRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$rhinoCode = Join-Path $env:ProgramFiles 'Rhino 8\System\rhinocode.exe'
$outDir = Join-Path $runtimeRoot 'runtime-state'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

if (-not (Test-Path $rhinoCode)) { throw "rhinocode not found at $rhinoCode" }
if (-not (Test-Path $JobSpec)) { throw "Job spec not found: $JobSpec" }

$job = Get-Content -Raw -Encoding UTF8 $JobSpec | ConvertFrom-Json
$allowList = @{
  'runtime_probe' = 'rhino\probe_runtime.py'
  'capture_evidence' = 'rhino\capture_evidence.py'
  'data_tree_cp2_cp4' = 'rhino\data_tree_cp2_cp4.py'
}

if (-not $allowList.ContainsKey([string]$job.job_type)) {
  throw "Job type '$($job.job_type)' is not allow-listed. Refusing arbitrary execution."
}

$scriptPath = Join-Path $runtimeRoot $allowList[[string]$job.job_type]
if (-not (Test-Path $scriptPath)) { throw "Allow-listed script missing: $scriptPath" }

$instancesRaw = & $rhinoCode list --json
if ($LASTEXITCODE -ne 0 -or -not $instancesRaw) {
  throw 'No Rhino script-server response. Run bootstrap_windows.ps1 and healthcheck.ps1 first.'
}
try { $instances = @($instancesRaw | ConvertFrom-Json) } catch { throw "Unable to parse rhinocode list --json: $($_.Exception.Message)" }
if ($instances.Count -eq 0) { throw 'No live Rhino script-server instance found.' }

$target = $instances[0]
if ($PipeId) {
  $candidate = $instances | Where-Object { $_.pipeId -eq $PipeId } | Select-Object -First 1
  if (-not $candidate) { throw "Requested Rhino pipeId '$PipeId' is not running." }
  $target = $candidate
}

$jobFullPath = [System.IO.Path]::GetFullPath($JobSpec)
$env:OLEANDER_RHINO_JOB = $jobFullPath
$env:OLEANDER_RHINO_OUT = $outDir

$dispatch = [ordered]@{
  timestamp = (Get-Date).ToString('o')
  job_type = [string]$job.job_type
  run_id = [string]$job.run_id
  script = $scriptPath
  job_spec = $jobFullPath
  target_pipe_id = $target.pipeId
  target_process_id = $target.processId
  status = 'DISPATCHING'
}
$dispatchPath = Join-Path $outDir 'dispatch_receipt.json'
$dispatch | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $dispatchPath

Write-Step "Dispatching job $($job.run_id) [$($job.job_type)] to Rhino process $($target.processId)..."
& $rhinoCode --rhino $target.pipeId script $scriptPath
$exitCode = $LASTEXITCODE

$dispatch.status = if ($exitCode -eq 0) { 'DISPATCH RETURNED ZERO' } else { 'DISPATCH FAILED' }
$dispatch.exit_code = $exitCode
$dispatch.completed_at = (Get-Date).ToString('o')
$dispatch | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $dispatchPath

if ($exitCode -ne 0) {
  throw "Rhino job returned exit code $exitCode. Inspect runtime-state outputs."
}

Write-Step "Job returned zero. This alone does NOT close evidence gates; inspect the job receipt and required outputs."
