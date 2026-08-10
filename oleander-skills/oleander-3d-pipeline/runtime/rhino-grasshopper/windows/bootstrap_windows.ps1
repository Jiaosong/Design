param(
  [string]$RuntimeRoot = "$PSScriptRoot\..",
  [int]$WaitSeconds = 45
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$Message) {
  Write-Host "[OLEANDER-RHINO] $Message"
}

function Read-RhinoInstances([string]$RhinoCodePath) {
  $raw = & $RhinoCodePath list --json 2>$null
  if ($LASTEXITCODE -ne 0 -or -not $raw) { return @() }
  try { return @($raw | ConvertFrom-Json) } catch { return @() }
}

$rhinoDir = Join-Path $env:ProgramFiles 'Rhino 8\System'
$rhinoExe = Join-Path $rhinoDir 'Rhino.exe'
$rhinoCode = Join-Path $rhinoDir 'rhinocode.exe'

if (-not (Test-Path $rhinoExe)) {
  throw "Rhino 8 not found at: $rhinoExe"
}
if (-not (Test-Path $rhinoCode)) {
  throw "rhinocode.exe not found. Rhino 8.11+ is required: $rhinoCode"
}

$version = (& $rhinoCode -V).Trim()
Write-Step "rhinocode version: $version"

try {
  $v = [version](($version -split '-')[0])
  if ($v.Major -lt 8 -or ($v.Major -eq 8 -and $v.Minor -lt 11)) {
    throw "Rhino 8.11+ required; found $version"
  }
} catch {
  throw "Unable to validate rhinocode version '$version': $($_.Exception.Message)"
}

if (-not (($env:Path -split ';') -contains $rhinoDir)) {
  $env:Path = "$rhinoDir;$env:Path"
  Write-Step 'Added Rhino 8 System directory to PATH for this PowerShell session.'
}

$instances = @(Read-RhinoInstances $rhinoCode)

if ($instances.Count -eq 0) {
  Write-Step 'No script-server Rhino instance detected. Starting Rhino 8 with StartScriptServer...'
  Start-Process -FilePath $rhinoExe -ArgumentList @(
    '/nosplash',
    '/notemplate',
    '/runscript="_StartScriptServer"'
  ) | Out-Null

  $deadline = (Get-Date).AddSeconds($WaitSeconds)
  do {
    Start-Sleep -Seconds 2
    $instances = @(Read-RhinoInstances $rhinoCode)
  } until (($instances.Count -gt 0) -or (Get-Date) -gt $deadline)
}

if ($instances.Count -eq 0) {
  throw "Rhino started but no rhinocode script-server instance became available within $WaitSeconds seconds. Open Rhino and run StartScriptServer manually, then retry."
}

$runtimeRootResolved = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$stateDir = Join-Path $runtimeRootResolved 'runtime-state'
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

$manifest = [ordered]@{
  status = 'HOST DETECTED'
  timestamp = (Get-Date).ToString('o')
  rhino_exe = $rhinoExe
  rhinocode_exe = $rhinoCode
  rhinocode_version = $version
  instances = $instances
  evidence_boundary = @(
    'This bootstrap proves only that a Rhino script-server instance is reachable by rhinocode.',
    'Grasshopper SDK, .gh solve, Parameter Viewer, canvas capture and viewport capture remain separate gates.'
  )
}

$manifestPath = Join-Path $stateDir 'bootstrap_manifest.json'
$manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $manifestPath
Write-Step "Bootstrap manifest written: $manifestPath"
Write-Step 'BOOTSTRAP PASS — proceed to healthcheck.ps1.'
