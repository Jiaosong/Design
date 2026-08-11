param(
  [Parameter(Mandatory=$true)][string]$RuntimeDll,
  [string]$EvidenceDir = "$PSScriptRoot\..\cp2_runtime_evidence",
  [string]$ProviderId = "P01_GUI_WINDOWS_DESKTOP"
)
$ErrorActionPreference='Stop'

$common = Join-Path $env:ProgramFiles 'Rhino 8\System\Rhino.exe'
$Rhino = if (Test-Path $common) { $common } else {
  $cmd=Get-Command Rhino.exe -ErrorAction SilentlyContinue
  if ($cmd) { $cmd.Source } else { $null }
}

New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
$EvidenceDir=(Resolve-Path $EvidenceDir).Path
$preflight=[ordered]@{
  exercise='SP02-R03 v1.4｜One-Run CP2 Closure'
  rhino_path=$Rhino
  runtime_dll=$RuntimeDll
  evidence_dir=$EvidenceDir
  provider_id=$ProviderId
  host_preflight='PENDING'
}

if (!$Rhino -or !(Test-Path $Rhino)) {
  $preflight.host_preflight='BLOCKED_RHINO_8_NOT_FOUND'
  $preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')
  throw 'Rhino 8 executable not found.'
}
if (!(Test-Path $RuntimeDll)) {
  $preflight.host_preflight='BLOCKED_RUNTIME_DLL_NOT_FOUND'
  $preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')
  throw "Runtime DLL not found: $RuntimeDll"
}

$RuntimeDll=(Resolve-Path $RuntimeDll).Path
$Script=(Resolve-Path "$PSScriptRoot\run_cp2_closure_in_rhino.py").Path
$env:SP02_RUNTIME_DLL=$RuntimeDll
$env:SP02_EVIDENCE_DIR=$EvidenceDir
$env:SP02_PROVIDER_ID=$ProviderId
$env:SP02_EXIT_AFTER_CP2='1'

$preflight.host_preflight='PASS'
$preflight.command='Rhino 8 /nosplash /notemplate /runscript=-_RunPythonScript(...)'
$preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')

# Rhino 8 officially supports /runscript and scripted -RunPythonScript at startup.
& $Rhino /nosplash /notemplate /runscript="-_RunPythonScript (`"$Script`")"
if ($LASTEXITCODE -ne 0) { throw "Rhino process exit code $LASTEXITCODE" }

& "$PSScriptRoot\..\validator\validate_cp2_receipts.ps1" -EvidenceDir $EvidenceDir
if ($LASTEXITCODE -ne 0) { throw "CP2 validator exit code $LASTEXITCODE" }
