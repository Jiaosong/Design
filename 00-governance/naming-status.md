# Naming and Status

Canonical file name:
`OLEANDER_[Scope]_[Node]_[ObjectID-or-Deliverable]_[Role]_vMAJOR.MINOR.PATCH_[Status]_[E#]_[YYYYMMDD].[ext]`

Scope: `SYS / C01 / C02 / C03 / PRAC`
Role: `SRC / WRK / TEST / EXP / REL / ARCH`

## Reserved case IDs

Bare case IDs are reserved exclusively for case roots:

- `C01` = 一脉广渡
- `C02` = 忘也 Daylily
- `C03` = The Light Collection / Reno CMF independent concept proposal

`C01`, `C02`, `C03`, and future bare `Cnn` values MUST NOT be used as Claim IDs, Evidence IDs, Asset IDs, Role IDs, experiment IDs, or node IDs.

Legacy aliases such as `CASE/GD`, `CASE/DY`, `CASE/LC`, `03|CASE/GD`, `P00`, and former `P01/P02/P03` project numbering may appear only in immutable source filenames, Legacy Alias fields, migration tables, or historical evidence references.

## Claim namespace

Canonical claim format:

`CLM-[Scope]-[NNN]`

Examples:

- `CLM-C01-001`
- `CLM-C02-001`
- `CLM-C03-001`
- `CLM-SYS-001`
- `CLM-MTH-001`

A bare `Cnn` in a Claim ID field is a migration failure.

Historical `CASE_GD_Public_Claim_Matrix.csv` IDs `C01–C05` map to `CLM-C01-001–005`; the historical bytes are not rewritten.

## File-state rule

Do not use `final`, `final-final`, `new`, `latest`, `copy`, or `副本` as authority-bearing state names.

When duplicate or superseded files exist, authority is determined by the canonical registry and immutable evidence reference, not by filename recency alone.
