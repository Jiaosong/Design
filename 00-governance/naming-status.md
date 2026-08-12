# Naming and Status

Canonical file name:
`OLEANDER_[Scope]_[Node]_[ObjectID-or-Deliverable]_[Role]_vMAJOR.MINOR.PATCH_[Status]_[E#]_[YYYYMMDD].[ext]`

Scope: `SYS / C01 / C02 / C03 / C04 / PRAC`
Role: `SRC / WRK / TEST / EXP / REL / ARCH`

A `Cnn` value in file Scope means **Case file scope only**. It does not become a P2 Project ID by appearing in a filename.

## Reserved case IDs

Bare case IDs are reserved exclusively for Canonical Case roots:

- `C01` = 一脉广渡
- `C02` = 忘也 Daylily
- `C03` = The Light Collection / Reno CMF independent concept proposal
- `C04` = 清江石书｜红花峰林十三印

`C01`, `C02`, `C03`, `C04`, and future bare `Cnn` values MUST NOT be used as Project IDs, Claim IDs, Evidence IDs, Asset IDs, Role IDs, experiment IDs, or generic node IDs.

Historical case-prefixed project-registry identities such as `C04-WS-* / C04-VAL-*` are migration residues. Preserve them where they are immutable provenance, but do not use them as templates for new P3/P4 identities. Repair the existing registry rows in place when the writable registry is recovered rather than creating duplicate projects.

Legacy aliases such as `CASE/GD`, `CASE/DY`, `CASE/LC`, `03|CASE/GD`, `P00`, and former `P01/P02/P03` project numbering may appear only in immutable source filenames, Legacy Alias fields, migration tables, or historical evidence references.

## Project axis namespace

Project hierarchy is reserved as:

`P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`

The hierarchy level and the Project ID are separate fields. Current Project IDs use explicit identities such as `PRJ-*`, `PG-*`, `PF-*`, `SYS-*` or `PRAC-*` according to object role; a Case ID does not substitute for them.

Delivery priority uses `Priority-0 / Priority-1 / Priority-2 / Priority-3`, never bare `P0/P1/P2/P3`.

## Application Mapping namespace

`B01–B04 / CU01–CU04 / IP01–IP04 / SP01–SP04` are Application Mapping codes. They are not Knowledge Architecture domains, Project IDs or delivery priorities. Knowledge ownership is resolved separately through `Domain / exact L0–L7 level`.

## Claim namespace

Canonical claim format:

`CLM-[Scope]-[NNN]`

Examples:

- `CLM-C01-001`
- `CLM-C02-001`
- `CLM-C03-001`
- `CLM-C04-001`
- `CLM-SYS-001`
- `CLM-MTH-001`

A bare `Cnn` in a Claim ID field is a migration failure.

Historical `CASE_GD_Public_Claim_Matrix.csv` IDs `C01–C05` map to `CLM-C01-001–005`; the historical bytes are not rewritten.

## File-state rule

Do not use `final`, `final-final`, `new`, `latest`, `copy`, or `副本` as authority-bearing state names.

When duplicate or superseded files exist, authority is determined by the canonical registry and immutable evidence reference, not by filename recency alone.
