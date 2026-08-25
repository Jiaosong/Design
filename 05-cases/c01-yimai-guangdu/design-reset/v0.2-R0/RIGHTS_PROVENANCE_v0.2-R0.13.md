# C01｜v0.2-R0.13｜Rights / Provenance Reconciliation

**Status:** `NO PUBLIC UPGRADE`  
**Existing P1/P2/P3 media:** `INTERNAL CONTROLLED USE / PUBLIC BLOCKED`

## What is now more precise

The current source chain no longer needs to describe every project-source image as simply `provenance unknown`.

### P1｜C1_zhenxiao.jpg
- file identity / SHA-256 / Drive ID: locked by the existing real-photo manifest;
- project-source DOCX order/caption mapping: `贞孝牌坊`;
- source family: the project compilation states the three-archway photographs use 潮新闻（钱江晚报）; an independent public visual index also records a Tide News Zhenxiao reference;
- exact original photograph / photographer / republication licence: **not closed**;
- public use: **BLOCKED**.

Decision: `PROVENANCE PARTIAL-CLOSED / RIGHTS OPEN`.

### P2｜C2_jiexiao.jpg
- file identity / SHA-256 / Drive ID: locked;
- project-source caption: `节孝牌坊`;
- source family: project compilation states Tide News source family;
- formal one-to-one identity `八股厅前 / 何氏节孝牌坊` remains separate from image-source reconciliation; generic official `广渡节孝牌坊` does not by itself close that mapping;
- exact photographer / reuse licence: **not closed**;
- public use: **BLOCKED**.

Decision: `PROVENANCE PARTIAL-CLOSED / OBJECT MAPPING HOLD / RIGHTS OPEN`.

### P3｜C2_maicai_detail.jpg
- file identity / SHA-256 / Drive ID: locked;
- project-source caption: `卖菜牌坊（大爿地）` detail;
- exact image provenance: **OPEN**;
- full elevation / spatial context: **OPEN**;
- rights: **OPEN**;
- public use: **BLOCKED**.

Decision: `DETAIL ONLY / PROVENANCE OPEN / PUBLIC BLOCKED`.

## Six boundaries

1. source family known ≠ exact-image provenance closed;
2. provenance closed ≠ reuse rights granted;
3. project caption mapping ≠ formal heritage identity;
4. public webpage visible ≠ permission to republish;
5. internal evidence use ≠ public media use;
6. P3 detail evidence ≠ full spatial evidence.

## Effect on R0 release status

No release upgrade is created.

R0-C01 / R0-C02 remain:
`INTERNAL ALLOW / PUBLIC-SAFE AFTER RESTRICTED IMAGE REMOVAL / PUBLIC BLOCK / v0.2-beta HOLD`.

Any future permission record must specify at least:
- rights holder / licensor;
- medium;
- territory;
- duration;
- attribution;
- modification permission;
- public / commercial scope;
- expiry / revocation where applicable.

Without that scope, an asset does not become `PUBLIC_READY`.