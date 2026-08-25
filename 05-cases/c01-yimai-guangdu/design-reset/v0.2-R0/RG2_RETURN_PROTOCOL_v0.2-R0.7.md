# C01｜v0.2-R0.7｜RG2 Return Intake Kit

**Status:** `READY FOR FIELD RETURN / NOT FIELD RESULT`

## Purpose

Field files must enter an auditable Evidence Record before they are bound into R0-C03 or any future Visitor Map.

## Minimum field sequence

### N06｜八角井
`Approach → Context → Close Read → Leave`

### N07｜古巷
`Public Passage → Threshold → Daily Use → Narrow Point → Private Visibility → Continue`

## Required metadata per file

- slot_id;
- source_id;
- original file name;
- SHA-256 when materialized;
- captured by;
- local capture time;
- specific location text;
- approach / leave direction;
- evidence coverage: what the file can and cannot support;
- observed current use: OBSERVED or UNKNOWN;
- public access confidence;
- stop / pass judgement;
- privacy risk;
- rights holder;
- publication permission;
- allowed use;
- reviewer and review date;
- final binding decision: `BIND_INTERNAL / BIND_PUBLIC / HOLD / REJECT`.

## Fail-closed rules

- `publication permission != YES` → cannot `BIND_PUBLIC`;
- privacy risk = `HIGH / UNKNOWN` → cannot `BIND_PUBLIC`;
- historical narrative cannot be used to infer current use;
- an open door does not imply permission to enter;
- a photograph does not imply permission to publish;
- no route is promoted to verified public path before RG2 continuity evidence closes it.

## Current gate

`RG2 NOT RUN / HUMAN TEST NOT RUN / CANONICAL POINTER RECOVERY OPEN`

This protocol is preparation only. It does not claim any field result.