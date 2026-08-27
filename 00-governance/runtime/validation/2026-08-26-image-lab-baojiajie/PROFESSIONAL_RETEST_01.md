# Image Lab｜Professional Retest 01

Date: 2026-08-27
Verdict: **I01–I06 REPAIR RETEST PASS / INDEPENDENT KEEP OPEN / ACTIVE NOT GRANTED**

The repaired runtime now treats output carrier, crop intent and source quality as explicit production inputs rather than assuming a fixed 1600×1200 canvas.

- I01 PASS — output role and target px/aspect ratio are explicit; 400×400 and 400×533 were both actually read back.
- I02 PASS — focal point is normalized to source coordinates, crop-safe is visible, COVER/CONTAIN/MANUAL are explicit and pointer drag changes focal coordinates.
- I03 PASS — baseline vs working shadow/highlight clipping is measured; extreme treatment produces `CHECK TONAL LOSS`.
- I04 PASS — normalized focal intent persists across 1:1 and 3:4 targets.
- I05 PASS — SPLIT mode shows true source-fit Before and current derivative simultaneously.
- I06 PASS — effective source resolution is measured. The reviewed 1200×1200 request uses only about 393×393 effective source pixels, enters `SOURCE_RESOLUTION_HOLD`, and PNG export is blocked by default. A 400×400 support crop is only `UPSCALE_CAUTION`, not a print-quality claim.

Persistent readback: `/Oleander/90_Archive/Runtime-Validation/2026-08-27/Image-Lab-Retest-01`.

Source Authority remains the original `1 (24).jpg`, SHA256 `e1d7fde5f7ac18b0a49b140e53d7dde95ee0e7295af56a3f0feb506bf3bc34b4`. The 400px derivative is a bounded digital support crop only. It is not a product hero, print-quality source, or new evidence.

This retest does not grant Independent KEEP. ACTIVE promotion remains withheld. `CI PASS ≠ professional/independent PASS`.
