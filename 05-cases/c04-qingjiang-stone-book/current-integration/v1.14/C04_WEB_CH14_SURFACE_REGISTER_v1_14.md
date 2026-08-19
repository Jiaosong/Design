# C04 Web v1.14｜CH14 Surface Register Correction

Project: `PRJ-C04-QINGJIANG-SHISHU`

## Trigger
The downstream Web incorrectly treated `CH14 P01–P07` as if seven source/system owners implied seven Web pages, and continued to describe the older v1.11 `112 surfaces` snapshot as the complete current carrier. This compressed the actual CH14 presentation inventory.

## Correct CH14 semantics

### 1. P01–P08 are authoring/system units, not one-page identities
Current CH14 authored base is `P01–P08` from `chapter-content-sync/v0.1/CH14_BRAND-VISUAL-IDENTITY.md`.

`P OWNER != ONE WEB PAGE`.

Main currently contains the P01–P07 source/executable baseline. P08 is an authored base unit whose dedicated source/materialization mapping remains open.

### 2. CH14 already has multi-surface execution evidence
P07 alone records `12 long-form brand-manual spec surfaces + scoped Web fragment`. Therefore any carrier that collapses P07 to one presentation surface is incomplete by construction unless an explicit PAGE REGISTER decision proves a different mapping.

P03/P04/P05/P06 also contain long-form manual/specimen systems and must be mapped by visible presentation role rather than counted mechanically from P labels.

### 3. Stone Seal v1.0 is a candidate family, not automatic Current pages
Draft PR #238 carries the current producer candidate `Stone Seal v1.0` and six page previews/contact evidence. It remains `INDEPENDENT DESIGN REVIEW PENDING / NO_PROMOTION`; those six previews are not silently promoted into canonical PAGE identities.

### 4. Seven CH14 expansion candidates remain explicit
- Brand Architecture
- Naming System
- Editorial System
- Motion Identity
- Photography Direction
- Illustration / Diagram Direction
- Material / Print

They are recoverable design scope, not auto-created Current pages.

## Carrier correction

- `v1.11 / 112 surfaces` = **STALE DOWNSTREAM SNAPSHOT / PRE-LATEST CHAPTER EXPANSION**.
- `v1.12` = CH14 visual-unification delta; it did not register the complete CH14 surface inventory.
- `v1.13` = CH07–CH09 currentization delta; preserve it unchanged, but it does not restore the missing CH14 register.
- `v1.14` = this semantic/register correction.

After v1.14, the Web must not answer `112` as the current complete Web carrier count.

Current integrated Web presentation-surface count is therefore:

> **NOT_YET_REGISTERED**

until the chapter-by-chapter surface register is rebuilt from current authored/source/candidate states and reconciled with the canonical PAGE REGISTER process.

This does not mean content is missing from the project. It means the downstream carrier count was stale and must not overwrite newer chapter production.

## Mandatory no-compression rules

`CHAPTER != PAGE`  
`AUTHORING UNIT != WEB SURFACE`  
`P OWNER != ONE PAGE`  
`CANDIDATE FAMILY != CURRENT PAGE IDENTITY`  
`NO COMPRESSION / NO LOSS`

## Preserved locks

- `ROUTE-03 = LOCKED CURRENT / NO GEOMETRY MUTATION`
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`
- `R06 = FINISHED / FROZEN / NO REOPEN`
- App remains a separate authority; Web consumes it downstream.

## Gate boundary
This correction repairs retrieval/carrier semantics and protects CH14 content from compression. It does not self-award Brand/Web Design PASS, create final canonical PAGE IDs, or promote Draft candidate families.

`INDEPENDENT FINISHED-PIXEL DESIGN VERDICT = PENDING`

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
