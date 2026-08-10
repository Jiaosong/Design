# OLEANDER / 织作 — SP04-R04 Constructability Stress Test

**Status: ACTUALLY EXECUTED / PASS**

Layer: Spatial / SP04 — Construction & Operation.

R04 asks a different question from R03:
**When should the system refuse to generate a geometrically valid opening?**

## Executed test families
- host-edge ligament sweep;
- opening-to-opening gap sweep;
- rounded-corner radius sweep;
- semicircular / shallow / tall arch cases;
- wall-thickness sweep;
- 2–12 opening array;
- six illegal-input rejection cases.

## Training-only rule engine
This package uses hypothetical rules only. They are not building codes, manufacturer requirements, structural criteria, or statutory tolerances.

Key rule hypotheses:
- edge ligament >= max(50 mm, 0.50 × wall thickness);
- opening gap >= max(100 mm, 0.75 × wall thickness);
- corner radius / wall thickness < 0.10 => WARNING;
- corner radius / wall thickness < 0.02 => FAIL;
- wall thickness < 40 mm => WARNING;
- wall thickness < 20 mm => FAIL;
- opening count > 8 => WARNING.

## Executed boundaries
- Edge ligament: {'last_pass': 120, 'first_warning': None, 'first_fail': 100}
- Opening gap: {'last_pass': 180, 'first_warning': None, 'first_fail': 160}
- Corner radius: {'last_pass': 24, 'first_warning': 20, 'first_fail': 4}
- Wall thickness: {'last_pass': 40, 'first_warning': 30, 'first_fail': 19}
- Opening array count: {'last_pass': 8, 'first_warning': 9, 'first_fail': None}

## Result
Illegal inputs rejected: 6/6.
Internal review: **99/100**.

Candidate decision:
**SP04 Constructability Candidate — TRAINING RULESET ONLY.**

This is stronger than the R03 geometric candidate, but it still does not establish structural adequacy, building-code compliance, manufacturer feasibility, BIM/IFC semantics, or construction approval.
