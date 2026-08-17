# OLEANDER Reference Materialization Gate v1.0

Status: **ACTIVE CURRENT**  
Scope: **ALL OLEANDER projects / all conversations / all reference-reconstruction work**

## 0｜Problem this gate solves

A source can be visible in a browser, Web/PDF viewer or connector and still be unavailable as local bytes to the execution runtime that must perform deterministic reconstruction QA.

`BROWSER_VISIBLE ≠ LOCAL_SOURCE_BYTES_AVAILABLE`

A citation ref, browser view id, screenshot handle or connector preview is not automatically a local file path. Python, SVG tooling, Blender, FFmpeg and pixel-diff tooling cannot honestly compare against a source until the source bytes or an exact locked reference frame are materialized into the execution runtime.

This gate closes that gap before a task may claim `1:1 REPRODUCTION`.

---

## 1｜Mandatory pre-reconstruction sequence

For any OLEANDER task that uses the words **reproduction / reconstruction / 复现 / 1:1**, execute this sequence before design work begins:

`SOURCE AUTHORITY FOUND → SOURCE BYTES MATERIALIZED → SOURCE HASHED → REFERENCE FRAME EXTRACTED → REFERENCE SCALE LOCKED → COMPARISON RUNTIME VERIFIED → 1:1 RECONSTRUCTION`

If any mandatory stage cannot be completed, stop only the fidelity claim and mark:

`REFERENCE MATERIALIZATION GATE = HOLD`

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
- `HOLD_SOURCE_AMBIGUOUS` — the exact source/version/frame is not uniquely resolved.

Do not write `MATERIALIZED` from a citation, screenshot id or browser view alone.

---

## 5｜Fidelity comparison after materialization

Only after the gate is closed may the Reference Reconstruction Fidelity Gate run:

`LOCKED ORIGINAL FRAME → 1:1 RECONSTRUCTION → MATCHED-SCALE SIDE-BY-SIDE → OVERLAY / FLICKER → DIFFERENCE VIEW → MISMATCH LIST → REPAIR → RE-TEST`

Use pixel difference together with geometry/visual judgment. Small antialiasing, rasterizer, ICC/color-management or font-rendering differences may be documented, but they cannot excuse material mismatches in composition, geometry, crop, type metrics, spacing, lineweight, object placement, lighting, camera or timing.

---

## 6｜Rights and truth boundary

Materialization proves only that a specific byte source was acquired and locked for comparison.

It does **not** prove:

- Source Authority;
- rights clearance or commercial reuse permission;
- reconstruction fidelity;
- design quality;
- field/engineering truth.

Reference copies remain study/calibration evidence unless a project's rights authority says otherwise. The copied reference artifact is not an OLEANDER original deliverable.

---

## 7｜Execution receipt fields

Any reference-reconstruction run should be able to report:

`SOURCE_AUTHORITY / SOURCE_LOCATOR / SOURCE_BYTES_STATE / SOURCE_SHA256 / REFERENCE_FRAME_STATE / PAGE_OR_FRAME / SCALE_OR_DPI / RENDERER / REFERENCE_FRAME_SHA256 / COMPARISON_RUNTIME / FIDELITY_GATE / DOES_NOT_PROVE`

If `SOURCE_BYTES_STATE != MATERIALIZED`, `REPRODUCTION PASS` is forbidden.

---

## 8｜Failure behavior

Do not wait for the end of a reconstruction to discover that overlay/diff is impossible. The materialization gate is a **preflight gate**.

When source bytes cannot be obtained:

1. record the exact blocker;
2. preserve the source locator and visible evidence;
3. continue only as a non-1:1 study if useful;
4. keep `FIDELITY HOLD`;
5. never lower the meaning of the word `reproduction` to make the task appear complete.
