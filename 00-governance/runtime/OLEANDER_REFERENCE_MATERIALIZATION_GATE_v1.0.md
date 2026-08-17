# OLEANDER Reference Materialization Gate v1.0

Status: **ACTIVE CURRENT**  
Scope: **ALL OLEANDER projects / all conversations / all reference-reconstruction work**

## 0｜Problem this gate solves

A source can be visible in a browser, Web/PDF viewer or connector and still be unavailable as local bytes to the execution runtime that must perform deterministic reconstruction QA.

`BROWSER_VISIBLE ≠ LOCAL_SOURCE_BYTES_AVAILABLE`

A citation ref, browser view id, screenshot handle or connector preview is not automatically a local file path. Python, SVG tooling, Blender, FFmpeg and pixel-diff tooling cannot honestly compare against a source until the source bytes or an exact locked reference frame are materialized into the execution runtime.

This gate closes that gap before a task may claim `1:1 REPRODUCTION`.

For OLEANDER, **reproduction / reconstruction / 复现 / 复刻 / 1:1 / 一模一样 / 按原图做** defaults to **pixel-level fidelity**. “Looks similar” or “visually close” is not enough.

---

## 1｜Mandatory pre-reconstruction sequence

For any OLEANDER task that claims reproduction, execute this sequence before design work begins:

`SOURCE AUTHORITY FOUND → SOURCE BYTES MATERIALIZED → SOURCE HASHED → REFERENCE FRAME EXTRACTED → REFERENCE SCALE LOCKED → COMPARISON RUNTIME VERIFIED → INDEPENDENT 1:1 RECONSTRUCTION → PIXEL-LEVEL COMPARISON → MISMATCH REPAIR → RETEST`

If any mandatory stage cannot be completed, stop only the fidelity claim and mark:

`REFERENCE MATERIALIZATION / FIDELITY GATE = HOLD`

The task may continue as `STRUCTURAL RECONSTRUCTION / METHOD STUDY / REFERENCE-BOUND STUDY`, but must not be promoted as `REPRODUCTION PASS`.

---

## 2｜Materialization routes

Resolve the first valid route that preserves the original source:

1. **Conversation upload / mounted file** — use the exact mounted local path.
2. **Public direct URL** — download the original file to the execution runtime; do not substitute a browser screenshot when source bytes are obtainable.
3. **Connector-native file** — use the connector's supported materialize/download action when bytes are needed locally.
4. **GitHub / Google Drive / repository source** — retrieve the exact identified file/version, then materialize locally when pixel/geometry comparison requires bytes.
5. **Browser-only source with no byte bridge** — record the source and set `HOLD_NO_SOURCE_BYTES`; do not fabricate missing pixels or dimensions.

A web page screenshot can be a locked reference frame only when the page itself is the authoritative visual surface and the capture dimensions, DPR/scale and state are known. It does not replace an obtainable original PDF/image/video/model file.

---

## 3｜Canonical runtime adapter

Preferred deterministic helper:

`python 90-shared/toolchains/reference-materialization/materialize_reference.py ...`

Examples:

```bash
# Public PDF
python 90-shared/toolchains/reference-materialization/materialize_reference.py \
  --url 'https://official.example/reference.pdf' \
  --out-dir /mnt/data/reference-lock \
  --page 12 \
  --dpi 200

# Existing local source
python 90-shared/toolchains/reference-materialization/materialize_reference.py \
  --file /mnt/data/source/reference.pdf \
  --out-dir /mnt/data/reference-lock \
  --page 12 \
  --dpi 200
```

The helper records:

- original source URL or local source path;
- materialized filename;
- byte count;
- SHA-256;
- detected content type;
- locked PDF page number when applicable;
- render DPI;
- renderer used;
- locked-frame pixel dimensions;
- locked-frame SHA-256;
- `does_not_prove` boundaries.

For PDF page locking, the adapter resolves `pdftoppm` first and `pypdfium2` second. If neither renderer is available, it fails closed rather than pretending a reference frame exists.

---

## 4｜Required manifest

Every materialized reference used for fidelity comparison must produce a machine-readable receipt such as:

`reference_materialization_manifest.json`

Minimum states:

- `MATERIALIZED` — source bytes exist locally and have a SHA-256;
- `LOCKED_REFERENCE_FRAME` — an exact page/frame has been rendered/extracted with recorded scale;
- `HOLD_NO_SOURCE_BYTES` — the source is visible/referenced but cannot be materialized;
- `HOLD_NO_RENDERER` — bytes exist but the required deterministic reference-frame render is unavailable;
- `HOLD_SOURCE_AMBIGUOUS` — the exact source/version/frame is not uniquely resolved;
- `HOLD_NO_PIXEL_COMPARISON` — a locked pixel-level comparison cannot be executed;
- `REVISE_PIXEL_MISMATCH` — material pixel mismatch remains;
- `PASS_PIXEL_LEVEL_FIDELITY` — pixel-level comparison is complete and no material mismatch remains.

Do not write `MATERIALIZED` from a citation, screenshot id or browser view alone.

---

## 5｜Pixel-level Fidelity Gate

Only after materialization is closed may the reconstruction fidelity gate run:

`LOCKED ORIGINAL FRAME → INDEPENDENT 1:1 RECONSTRUCTION → MATCHED-SCALE SIDE-BY-SIDE → PIXEL-ALIGNED OVERLAY / FLICKER → PIXEL DIFFERENCE → GEOMETRY / TYPE / SPACING MISMATCH LIST → REPAIR → PIXEL RE-TEST`

### Default target

The default target is:

**`PIXEL_IDENTICAL_AT_LOCKED_REFERENCE_SCALE_OR_FRAME`**

For deterministic vector, raster, icon, interface-frame or page reconstruction using the same deterministic render pipeline, target **zero pixel difference**.

For 3D, motion or other media where renderer, antialiasing, ICC/color-management or font rasterization can introduce non-design noise, those differences may be accepted only when they are:

1. isolated from design/geometry differences;
2. quantitatively measured;
3. visually inspected;
4. shown not to hide mismatch in composition, geometry, crop, type metrics, spacing, lineweight, object placement, material, lighting, camera, timing or motion path.

If that proof cannot be made, the result stays `REVISE` or `HOLD`.

### Reconstruction independence

A zero pixel diff obtained by copying, embedding, tracing through direct source reuse, or simply re-exporting the original source bytes is **not reconstruction evidence**.

A claimed reconstruction must have an independently constructed editable representation appropriate to the medium. The purpose of the fidelity exercise is to prove that the design can be reconstructed, not that the original file can be duplicated.

### Mandatory matching dimensions

Match as applicable:

- canvas / frame / aspect ratio / crop;
- geometry / silhouette / object placement;
- grid / margins / alignment / spacing / whitespace;
- type family or closest legally/technically available equivalent, size, weight, leading, tracking, line breaks and baseline behavior;
- lineweight / stroke / icon / pictogram / annotation geometry;
- image scale / crop / tone / color / contrast;
- material / lighting / camera / lens / perspective for 3D and spatial/product work;
- timing / easing / path / overlap / key-frame relations for motion and interaction.

“Similar”, “same principle”, “same hierarchy”, “same style”, “visually close”, or “looks indistinguishable at a glance” does not satisfy this gate without pixel-level evidence.

---

## 6｜Pass / Revise / Hold behavior

### `REPRODUCTION PASS`

Allowed only when:

- source bytes are materialized;
- reference frame and scale are locked;
- the reconstruction is independently constructed;
- pixel-level comparison is executed;
- no material pixel mismatch remains;
- deterministic media reach zero diff where technically achievable;
- any unavoidable render noise is isolated and quantified;
- final repair is followed by a final re-test.

### `REVISE`

Use when the structure is correct but any material mismatch remains in pixels, geometry, typography, crop, lineweight, spacing, color, material, camera, lighting or timing.

### `HOLD`

Use when source bytes, exact frame, comparison scale, renderer, comparison runtime, or pixel-level evidence cannot be established honestly.

Do not downgrade the meaning of reproduction to escape runtime limits.

---

## 7｜Rights and truth boundary

Materialization and pixel-level fidelity prove only that a specific reference was acquired, locked and reconstructed with the stated fidelity.

They do **not** prove:

- Source Authority unless separately established;
- rights clearance or commercial reuse permission;
- independent design quality of the copied work;
- field/engineering truth;
- quality of a later transfer variant.

Reference copies remain study/calibration evidence unless a project's rights authority says otherwise. The copied reference artifact is not an OLEANDER original deliverable.

---

## 8｜Execution receipt fields

Any reference-reconstruction run should be able to report:

`SOURCE_AUTHORITY / SOURCE_LOCATOR / SOURCE_BYTES_STATE / SOURCE_SHA256 / REFERENCE_FRAME_STATE / PAGE_OR_FRAME / SCALE_OR_DPI / RENDERER / REFERENCE_FRAME_SHA256 / COMPARISON_RUNTIME / PIXEL_DIFF_STATE / PIXEL_DIFF_METRIC / MISMATCH_STATE / FIDELITY_GATE / DOES_NOT_PROVE`

If `SOURCE_BYTES_STATE != MATERIALIZED`, `REPRODUCTION PASS` is forbidden.

If pixel-level comparison was not executed, `REPRODUCTION PASS` is forbidden.

If material pixel mismatch remains, `REPRODUCTION PASS` is forbidden.

---

## 9｜Failure behavior

Do not wait for the end of a reconstruction to discover that overlay/diff is impossible. Materialization and comparison-runtime verification are **preflight gates**.

When source bytes or pixel-level comparison cannot be obtained:

1. record the exact blocker;
2. preserve the source locator and visible evidence;
3. continue only as a non-1:1 study if useful;
4. keep `FIDELITY HOLD`;
5. never lower the meaning of the word `reproduction` to make the task appear complete.
