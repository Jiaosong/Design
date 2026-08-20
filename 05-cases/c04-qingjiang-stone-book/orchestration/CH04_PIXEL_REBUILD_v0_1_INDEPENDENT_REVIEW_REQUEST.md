# CH04 Pixel Web Reconstruction v0.1｜Independent Review Request

Review mode: `INDEPENDENT / READ-ONLY / NO PRODUCER SELF-PASS`.

## Review target

`PRJ-C04-QINGJIANG-SHISHU → CH04-P01…P06 → Pixel Web Reconstruction v0.1`.

User intent: stop new image generation and turn the approved visual direction into a real webpage using the OLEANDER reconstruction discipline.

## Required review evidence

Open the actual package/readbacks and inspect:

1. six browser-rendered pages at the locked `1672×941` frame;
2. P01/P02/P04/P05 matched reference/candidate/diff views;
3. 1366×768 and 390×844 scaling behavior;
4. navigation/keyboard focus and offline dependency state;
5. authority preservation for P03 `ROUTE-03` and P06 R06.

## Mandatory judgments

For each P01–P06 and overall, return:

- `KEEP / REVISE / REJECT / HOLD`;
- one primary Root Cause;
- First Visual Gate `PASS / FAIL`;
- Professional Finish Gate `PASS / FAIL`;
- whether the result reads as a real webpage rather than a screenshot pasted into a browser;
- whether raster/reference carrier use is acceptably bounded and explicitly separated from geometry/design authority;
- whether any page regresses into dashboard / diagram-first presentation.

## Fidelity boundary

The producer measured pixel error but does **not** claim full independent reproduction. P01/P02/P04/P05 use bounded reference visual carriers; the reconstructed and independently editable portion is the webpage frame/chrome/assembly. OLEANDER `REVIEW.md` therefore keeps full independent reproduction at `HOLD`.

## Persistence blocker

Binary package hash is known, but durable remote binary persistence is currently `UNSYNCED` in this connector session. Do not promote while the binary package is not independently recoverable from durable project storage.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
