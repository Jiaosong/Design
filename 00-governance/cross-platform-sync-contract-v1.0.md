# OLEANDER Cross-platform Sync Contract v1.0

Status: ACTIVE
Date: 2026-08-13
Scope: Notion, GitHub and Google Drive synchronization claims for OLEANDER governance, knowledge, practice, project and release artifacts.

## Core rule

**Write success != Sync success. Readback-confirmed canonical persistence = SYNCED.**

A platform may be reported as `SYNCED` only after the target-platform readback gate passes. Artifact generation, local save, API success, upload success, commit creation, CI PASS, PR OPEN or MERGED are intermediate facts only.

## Google Drive chain

`Artifact Generated → Local Open Test → Connector-compatible File Reference → Drive Upload → Drive Readback → SYNCED`

- `Artifact Generated`: final artifact exists and is non-empty / non-placeholder.
- `Local Open Test`: reopen or parse the final artifact and confirm expected structure/content.
- `Connector-compatible File Reference`: obtain a file reference accepted by the Drive connector; a local path alone is not upload evidence.
- `Drive Upload`: actually upload/import/update the artifact into the existing canonical `OLEANDER_Project-Archive` path.
- `Drive Readback`: re-read the target Drive file/folder and confirm file existence, name, parent, type and necessary content.
- Only `Drive Readback PASS` permits `GOOGLE DRIVE SYNCED`, `ARCHIVED` or `SYNC COMPLETE`.

## GitHub chain

`Artifact Generated → Local Open Test → Repo-compatible Artifact → Commit / Push → Remote Readback → SYNCED`

- `Artifact Generated`: final artifact exists and is non-empty / non-placeholder.
- `Local Open Test`: reopen or parse the final artifact and confirm expected structure/content.
- `Repo-compatible Artifact`: verify canonical path, naming, file format, sensitivity, size and version-control suitability. Dynamic quotations, field/project truth, sensitive data or unsuitable large binaries must not be forced into Git merely to claim complete synchronization.
- `Commit / Push`: a real commit must reach the intended remote branch. A local-only commit does not constitute GitHub synchronization.
- `Remote Readback`: re-read the remote commit/tree/blob or target file from GitHub and verify commit SHA, branch, canonical path, file existence and necessary content.
- Only `Remote Readback PASS` permits `GITHUB SYNCED` or `REMOTE SYNC COMPLETE`.

### GitHub failure states

- `GENERATED → LOCAL OPEN PASS → REPO EGRESS BLOCKED → GITHUB PENDING`
- `GENERATED → LOCAL OPEN PASS → REPO-COMPATIBLE PASS → COMMIT/PUSH FAIL → GITHUB SYNC FAILED`
- `GENERATED → LOCAL OPEN PASS → COMMIT/PUSH PASS → REMOTE READBACK FAIL → SYNC UNCONFIRMED`

`COMMIT CREATED`, `CI PASS`, `PR OPEN` and `MERGED` each prove only their own Git/CI/PR fact. None automatically proves that a specified artifact completed remote synchronization readback.

## Notion chain

`Knowledge / Record Generated → Schema & Canonical Target Check → Notion Write → Notion Readback → SYNCED`

A successful Notion write call is insufficient by itself. The target page/record must be read back and the expected canonical target, key fields and necessary content must be present before `NOTION SYNCED` may be reported.

## Cross-platform reporting

Report each platform independently, for example:

`NOTION SYNCED / GITHUB PENDING / DRIVE SYNCED`

A single undifferentiated `SYNCED` status must not hide a partial failure.

## AR-S09 integration

AR-S09 Release Package Review includes this Cross-platform Sync Gate whenever the package claims persistence to Notion, GitHub or Drive.

- GitHub sync claims require the complete GitHub chain through `Remote Readback PASS`.
- Drive sync claims require the complete Drive chain through `Drive Readback PASS`.
- Notion sync claims require `Notion Readback PASS`.
- Production binaries continue to trigger the independent `Production Asset Persistence Gate v1.0`; this Sync Contract does not replace PAP-G0—PAP-G6.

## Canonical principle

**Target-platform readback is the final synchronization gate.**
