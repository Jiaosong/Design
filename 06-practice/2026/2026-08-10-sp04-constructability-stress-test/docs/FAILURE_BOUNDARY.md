# SP04-R04 Failure Boundary

All rules in this document are training hypotheses.

## Edge ligament
{'last_pass': 120, 'first_warning': None, 'first_fail': 100}

The governing hypothetical requirement is:
`max(50 mm, 0.50 × wall thickness)`.

## Opening gap
{'last_pass': 180, 'first_warning': None, 'first_fail': 160}

The governing hypothetical requirement is:
`max(100 mm, 0.75 × wall thickness)`.

## Corner radius
{'last_pass': 24, 'first_warning': 20, 'first_fail': 4}

Two-stage policy:
- ratio < 0.10 => WARNING;
- ratio < 0.02 => FAIL.

## Wall thickness
{'last_pass': 40, 'first_warning': 30, 'first_fail': 19}

Two-stage policy:
- thickness < 40 mm => WARNING;
- thickness < 20 mm => FAIL.

## Opening count
{'last_pass': 8, 'first_warning': 9, 'first_fail': None}

Count alone does not create a geometric failure in this training model; it is used as an operational-complexity warning beyond 8 openings.

## Meaning of status
- PASS: geometry passes and no current training constructability rule is triggered.
- WARNING: geometry is valid but a constructability caution is triggered.
- FAIL: geometry is invalid or a training hard-rule threshold is crossed.
