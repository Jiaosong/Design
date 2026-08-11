param(
  [Parameter(Mandatory=$true)][string]$EvidenceDir,
  [string]$ExpectedContract = "$PSScriptRoot\..\..\contracts\expected_tree_contract.json"
)
$ErrorActionPreference='Stop'

$EvidenceDir=(Resolve-Path $EvidenceDir).Path
$ExpectedContract=(Resolve-Path $ExpectedContract).Path
$errors = New-Object System.Collections.Generic.List[string]

function Read-Json([string]$name) {
  $p=Join-Path $EvidenceDir $name
  if (!(Test-Path $p)) { $errors.Add("MISSING $name"); return $null }
  try { return Get-Content $p -Raw | ConvertFrom-Json }
  catch { $errors.Add("INVALID_JSON $name : $($_.Exception.Message)"); return $null }
}
function Json-Compact($x) { return ($x | ConvertTo-Json -Compress -Depth 50) }
function Same-Array($a,$b) { return (Json-Compact @($a)) -eq (Json-Compact @($b)) }

$provider=Read-Json 'provider_receipt.json'
$definition=Read-Json 'definition_receipt.json'
$solve=Read-Json 'solve_receipt.json'
$tree=Read-Json 'tree_runtime.json'
$repro=Read-Json 'reproduction_receipt.json'
$expected=Get-Content $ExpectedContract -Raw | ConvertFrom-Json

$micro=[ordered]@{
  SG00='OPEN'; SG01='OPEN'; SG02='OPEN'; SG03='OPEN'; SG04='OPEN'; SG05='OPEN'; SG06='OPEN'; SG07='OPEN'
}

if ($provider -and $provider.runtime_authority_verified -eq $true -and $provider.provider_id -and $provider.execution_id -and $provider.truth_state -eq 'REAL_RHINO_GRASSHOPPER_RUNTIME') {
  $micro.SG00='PASS'
} else { $errors.Add('SG00 provider authority receipt invalid or Rhino license not validated') }

$native=Join-Path $EvidenceDir 'SP02_R03_native.ghx'
if ($definition -and (Test-Path $native)) {
  $sha=(Get-FileHash $native -Algorithm SHA256).Hash.ToLower()
  $required=@('SP02_BASE','SP02_GRAFT','SP02_FLATTEN','SP02_TRANSPOSE','SP02_ADVERSE_TRANSPOSE','PV_BASE','PV_GRAFT','PV_FLATTEN','PV_TRANSPOSE','PV_ADVERSE')
  $identity=$true
  foreach($n in $required) {
    $v=$definition.nickname_inventory.$n
    if ($v -ne 1) { $identity=$false; $errors.Add("SG01 nickname inventory invalid: $n = $v") }
  }
  if ($definition.runtime_state -eq 'REAL_GRASSHOPPER_SERIALIZE_AND_RELOAD' -and $definition.save_success -eq $true -and $definition.load_success -eq $true -and $definition.sha256 -eq $sha -and $identity) {
    $micro.SG01='PASS'
  } else { $errors.Add('SG01 native definition serialize/reload/hash evidence invalid') }
} else { $errors.Add('SG01 definition receipt or native GHX missing') }

if ($solve -and $solve.request_observed -eq $true -and $solve.mechanism -match 'GH_Document.NewSolution') { $micro.SG02='PASS' }
else { $errors.Add('SG02 solve request evidence invalid') }

if ($solve -and $solve.completion_observed -eq $true -and @($solve.errors).Count -eq 0 -and $solve.output_fingerprint) { $micro.SG03='PASS' }
else { $errors.Add('SG03 solve completion/errors/output fingerprint invalid') }

$requiredStates=@('BASE','GRAFT','FLATTEN','TRANSPOSE','ADVERSE_TRANSPOSE')
$haveStates=$tree -ne $null
if ($haveStates) {
  foreach($s in $requiredStates) { if ($null -eq $tree.states.$s) { $haveStates=$false } }
}
if ($haveStates) { $micro.SG04='PASS' } else { $errors.Add('SG04 five tree states not all present') }

function Check-State($obs,$target,[string]$name) {
  if ($null -eq $obs) { return $false }
  $ok=$true
  if ([int]$obs.branch_count -ne [int]$target.branch_count) { $ok=$false }
  if ([int]$obs.data_count -ne [int]$target.data_count) { $ok=$false }
  if (!(Same-Array $obs.branch_lengths $target.branch_lengths)) { $ok=$false }
  if ($null -ne $target.paths -and !(Same-Array $obs.paths $target.paths)) { $ok=$false }
  if (!$ok) { $errors.Add("State contract mismatch: $name") }
  return $ok
}

$nominalOk=$false
if ($micro.SG04 -eq 'PASS') {
  $nominalOk = (Check-State $tree.states.BASE $expected.nominal.BASE 'BASE') -and
               (Check-State $tree.states.GRAFT $expected.nominal.GRAFT 'GRAFT') -and
               (Check-State $tree.states.FLATTEN $expected.nominal.FLATTEN 'FLATTEN') -and
               (Check-State $tree.states.TRANSPOSE $expected.nominal.TRANSPOSE 'TRANSPOSE')
}
if ($nominalOk) { $micro.SG05='PASS' }

$adverseOk=$false
if ($micro.SG04 -eq 'PASS') {
  $adverseOk=Check-State $tree.states.ADVERSE_TRANSPOSE $expected.adverse.ADVERSE_TRANSPOSE 'ADVERSE_TRANSPOSE'
}
if ($adverseOk) { $micro.SG06='PASS' }

if ($repro -and [int]$repro.run_count -ge 2 -and $repro.definition_hash_same -eq $true -and $repro.structure_signature_match -eq $true) { $micro.SG07='PASS' }
else { $errors.Add('SG07 repeatability receipt invalid') }

$cp2 = if (@($micro.Values | Where-Object { $_ -ne 'PASS' }).Count -eq 0) {'PASS'} else {'OPEN'}
$result=[ordered]@{
  exercise='SP02-R03 v1.4｜One-Run CP2 Closure'
  microgates=$micro
  CP2_CORE=if ($micro.SG00 -eq 'PASS' -and $micro.SG01 -eq 'PASS' -and $micro.SG02 -eq 'PASS' -and $micro.SG03 -eq 'PASS') {'PASS'} else {'OPEN'}
  CP2_DATA=if ($micro.SG04 -eq 'PASS' -and $micro.SG05 -eq 'PASS' -and $micro.SG06 -eq 'PASS') {'PASS'} else {'OPEN'}
  CP2_REPRO=if ($micro.SG07 -eq 'PASS') {'PASS'} else {'OPEN'}
  CP2=$cp2
  CP4='OPEN'
  errors=@($errors)
  practice_close_allowed=$false
  truth='A real Rhino execution may close CP2 in one run; CP4 remains independent GUI provenance.'
}
$result | ConvertTo-Json -Depth 50 | Set-Content -Encoding UTF8 (Join-Path $EvidenceDir 'CP2_VALIDATION_RESULT.json')
$result | ConvertTo-Json -Depth 50
if ($cp2 -ne 'PASS') { exit 2 }
