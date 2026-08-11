param(
  [Parameter(Mandatory=$true)][string]$BuilderDll,
  [string]$EvidenceDir = "$PSScriptRoot\..\native_definition_evidence"
)
$ErrorActionPreference = 'Stop'

$Rhino = Join-Path $env:ProgramFiles 'Rhino 8\System\Rhino.exe'
$Script = (Resolve-Path "$PSScriptRoot\run_builder_in_rhino.py").Path
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
$EvidenceDir = (Resolve-Path $EvidenceDir).Path

$preflight = [ordered]@{
  gate='SG01'
  rhino_path=$Rhino
  builder_dll=$BuilderDll
  evidence_dir=$EvidenceDir
  host_preflight='PENDING'
}

if (!(Test-Path $Rhino)) {
  $preflight.host_preflight='BLOCKED_RHINO_8_NOT_FOUND'
  $preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')
  throw "Rhino 8 not found at $Rhino"
}
if (!(Test-Path $BuilderDll)) {
  $preflight.host_preflight='BLOCKED_BUILDER_DLL_NOT_FOUND'
  $preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')
  throw "Builder DLL not found: $BuilderDll"
}

$BuilderDll=(Resolve-Path $BuilderDll).Path
$GhOut=Join-Path $EvidenceDir 'SP02_R03_native.ghx'
$env:SP02_BUILDER_DLL=$BuilderDll
$env:SP02_GHX_OUT=$GhOut
$env:SP02_EXIT_AFTER_BUILD='1'

$preflight.host_preflight='PASS'
$preflight.rhino_version_source='Rhino process receipt follows after successful run'
$preflight | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'HOST_PREFLIGHT.json')

& $Rhino /nosplash /notemplate /runscript="-_RunPythonScript (`"$Script`")"
if ($LASTEXITCODE -ne 0) { throw "Rhino process exit code $LASTEXITCODE" }

python "$PSScriptRoot\..\validator\validate_sg01_definition_receipt.py" $EvidenceDir
