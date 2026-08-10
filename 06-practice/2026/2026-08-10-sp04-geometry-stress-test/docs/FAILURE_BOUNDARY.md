# R03 Failure Boundary

## Shape complexity
Rounded, arched, eccentric and three-opening mixed geometry all passed native topology plus OBJ/STL/GLB round-trip checks.

## Thin host ligament
- Rule preflight used for ordinary candidate work: 50.0 mm (training hypothesis only).
- Numerical stress sweep intentionally bypassed this rule.
- Last tested value preserved by all three formats: 0.0002 mm.
- First tested value failing explicit feature fidelity: 0.0001 mm.

## Multi-opening gap
- Rule preflight used for ordinary candidate work: 100.0 mm (training hypothesis only).
- Numerical stress sweep intentionally bypassed this rule.
- Last tested value preserved by all three formats: 0.0005 mm.
- First tested failure: 0.0002 mm.

## Mechanism observed
At coordinate magnitudes around 3000–3300 mm, NumPy reports float32 spacing of 0.000244140625 mm.
The STL/GLB loss of extremely small gaps/ligaments is consistent with coordinate quantization at that scale.
This is an inference from the executed runtime evidence, not a universal file-format design limit.

## QA rule added
Do not accept:
`watertight + volume pass + bbox pass`
as sufficient evidence.

R03 candidate gate adds:
`feature_fidelity == true`.
