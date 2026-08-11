param(
  [Parameter(Mandatory=$true)][string]$GhFile,
  [string]$EvidenceDir = "$PSScriptRoot\..\runtime_evidence"
)
$ErrorActionPreference = "Stop"
$Rhino = Join-Path $env:ProgramFiles "Rhino 8\System\Rhino.exe"
$Receipt = Join-Path $EvidenceDir "HOST_PREFLIGHT.json"
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

if (-not (Test-Path $Rhino)) {
  @{ runtime_state="HOST_BLOCKED"; reason="RHINO_8_NOT_FOUND"; rhino_path=$Rhino } |
    ConvertTo-Json | Set-Content -Encoding UTF8 $Receipt
  throw "Rhino 8 not found at $Rhino"
}
if (-not (Test-Path $GhFile)) {
  throw "Grasshopper definition not found: $GhFile"
}

$env:SP02_GH_FILE = (Resolve-Path $GhFile).Path
$env:SP02_EVIDENCE_DIR = (Resolve-Path $EvidenceDir).Path
$env:SP02_EXIT_AFTER_CAPTURE = "1"
$Capture = (Resolve-Path "$PSScriptRoot\..\rhino\SP02_R03_capture_runtime.py").Path

@{
  runtime_state="HOST_PREFLIGHT_PASS"
  rhino_path=$Rhino
  gh_file=$env:SP02_GH_FILE
  capture_script=$Capture
} | ConvertTo-Json | Set-Content -Encoding UTF8 $Receipt

& $Rhino /nosplash /notemplate /runscript="-_RunPythonScript (`"$Capture`")"
if ($LASTEXITCODE -ne 0) { throw "Rhino process exit code $LASTEXITCODE" }

python "$PSScriptRoot\..\validator\validate_runtime_evidence.py" $EvidenceDir
