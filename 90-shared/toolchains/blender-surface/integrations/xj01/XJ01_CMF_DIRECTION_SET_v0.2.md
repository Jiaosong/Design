# XJ01 CMF Direction Set 01 v0.2

Status: `R02-00 PASS / R02-01 A_MID SELECTED / R02-02A F_MID SELECTED / R02-02B PASS / R02-02C PASS / MATERIAL-PROCESS-FINISH-TEXTURE DIGITAL DEVELOPMENT OPEN`

This file records the current **digital CMF direction and lightweight sampling plan**. Heavy Blender renders, EXR files and portfolio boards remain in Google Drive; GitHub stores the auditable decision/spec contract only.

## 1. Selected digital direction

### Primary — Mineral Cool Blue

| Role | Digital color | Material fact | Current appearance/process direction |
|---|---|---|---|
| `MAT_PP_PRIMARY_FIELD` | `#92A9BA` | PP | injection-molded PP / fine matte |
| `MAT_PP_SECONDARY` | `#E4E1D9` | PP | same restrained PP family |
| `MAT_PP_UI` | `#31516A` | PP | darker local signal; subtle micro-etch/grip texture may be explored |
| `MAT_PU_CONTACT` | `#65737A` | PU | soft-matte dielectric response |
| `MAT_IRON_VISIBLE` | `#888C8F` | iron tube | fine-matte coated-tube sample direction |
| `MAT_METAL_HARDWARE` | `#777A78` | metal hardware | restrained satin metal |

### Alternate — Clean Teal

Primary Field `#8BACAA`; UI `#245E60`; PU `#617270`. Material/process architecture remains the same as the primary direction.

## 2. R02 decision chain

- `R02-01`: Anchor lightness — `A_MID #888C8F` selected after Whole Product + rod/PP-joint review.
- `R02-02A`: Field lightness — `F_MID #AAA59D` selected as the lightness corridor baseline.
- `R02-02B`: Hue — warm-neutral rejected; Cool Blue and Teal retained.
- `R02-02C`: Chroma — `C05` under-signals the Field; `C20` begins to dominate first reading; `C12` retained as the digital corridor for both hue families.
- Current primary = **Cool Blue C12 `#92A9BA`**.
- Current alternate = **Teal C12 `#8BACAA`**.

The selections above are designer digital calibration, not user-preference findings or production color approvals.

## 3. Surface / texture intent

Surface System: `OLEANDER Blender Surface System v1.15 | C Track Rendered`.

- Main PP uses the `PP_INJECTION_FINE_MATTE` / `NT_PP_FINE_MATTE` visual method. The Hero-scale target is broad, low-contrast highlight response rather than visible decorative grain.
- PP UI may use a restrained localized micro-etch/grip texture. It must remain subordinate to product form and color hierarchy; no leather-like decorative texture.
- PU should separate from PP through softer/higher-roughness response rather than exaggerated bump.
- Iron tube currently targets a fine-matte coated appearance. Powder coating is a practical sample hypothesis, not yet a verified XJ01 production finish.
- Hardware uses a satin-metal visualization baseline. Exact plating/coating remains open.

All numerical roughness, noise-scale and bump seeds remain `VISUALIZATION_HYPOTHESIS` until upgraded by sample/manufacturer/measurement evidence.

## 4. Portfolio evidence separation

1. `Controlled Evidence View` — locked R02 camera/light/exposure for controlled decisions.
2. `CMF Detail View` — local PP / PU / iron / hardware / interface reading.
3. `Portfolio Hero View` — independent 72 mm restrained 3/4 reflection-card presentation; never reused as R02 A/B evidence.
4. `Physical Sample View` — future real plaques/coupons/strips to close tactile/color/process gaps.

## 5. Lightweight physical sample plan

The mop does not require an oversized CMF validation matrix at this stage. Use a small decision-oriented set:

- **PP color plaques**: for each retained hue, nominal + slightly lighter/lower-chroma + slightly deeper/higher-chroma; about `80 × 120 mm` or larger when practical, preferably in the actual PP resin family.
- **PP surface plaques**: `S1 Fine Matte` and `S2 Local Micro-Etch`. Do not assign Mold-Tech / VDI / SPI numbers before supplier/tooling samples exist.
- **Iron tube coupon**: one `150–250 mm` real tube with `#888C8F` fine-matte coating; optionally one smoother comparison.
- **PU strip**: standard soft matte + slightly smoother/finer reference; main `#65737A`, alternate `#617270`.
- **Hardware**: use the existing production component first; develop a separate finish only if brightness disrupts the hierarchy.

First sample review checks only:
1. whole-product color hierarchy;
2. PP–PU separation;
3. iron-tube visual weight;
4. dirt/fingerprint visibility;
5. whether UI micro-etch reads intentional rather than decorative.

Do not expand the sample matrix unless one of these checks fails.

## 6. Evidence boundary

The current result is suitable for digital CMF direction setting and portfolio development. It does **not** validate final master color, physical gloss/roughness, wet/dirty/aged behavior, production tolerance, supplier capability, user preference or mass-production approval.
