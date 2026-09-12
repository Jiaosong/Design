# OLEANDER 3D Pipeline — Diagnostic Mask Validity Protocol v1

A projection metric is invalid if the diagnostic mask semantics are not independently verified.

## Preferred mask
For geometry silhouette screening use a dedicated mask render:
- only the intended final visible candidate family enabled;
- pure white emission material override;
- pure black world/background;
- no tone-dependent material response;
- no transparency ambiguity;
- persisted PNG/EXR read back after render.

Film alpha is not accepted as the sole mask signal unless a mask-validity test proves background=0 and object=1 for that runtime/backend.

## MUST CHECK
- mask contains both foreground and background;
- foreground coverage is plausible (default 2–80% unless task defines another range);
- bounding box is finite and not the full frame;
- known empty corner pixel is background;
- known candidate interior sample is foreground when resolvable;
- projection orientation is locked by camera convention, not chosen post hoc for lower error.

## FAIL
- `FAIL_PROJECTION_MASK_INVALID`
- `FAIL_PROJECTION_MASK_ALL_FOREGROUND`
- `FAIL_PROJECTION_MASK_ALL_BACKGROUND`
- `FAIL_PROJECTION_MASK_FRAME_CLIPPED`

V15 transfer: Cycles film-alpha diagnostics returned opaque/background behavior that caused every side sample to read the frame top as body. Beauty/model build was valid; the mask measurement was not. V16 switches to emission-mask RGB thresholding.
