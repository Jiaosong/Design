# TRANSFORMATION LOG

## A｜Source materialization
- Keep raw elevation sample CSV unchanged.
- Keep OSM Qingjiang context line unchanged.
- Record context corridor separately from scenic boundary.

## B｜DEM / slope / aspect
- Reshape 441 samples to 21×21 regular grid.
- Convert spacing to metric using EPSG:32649.
- Compute first derivatives.
- Slope = arctan(sqrt(dzdx² + dzdy²)).
- Aspect = compass bearing, 0=N.

## C｜Potential drainage
- D8 receiver: each sample routes to the lowest adjacent sample.
- Accumulation = upstream sampled-cell count.
- No rainfall-runoff coefficient, channel calibration, culvert data or hydraulic model.

## D｜Solar exposure
- Use terrain slope/aspect and simplified solar-noon geometry.
- Three scenarios: summer solstice / equinox / winter solstice.
- Figure shows relative terrain incidence, not measured radiation.

## E｜Land cover
- No substitute classification was generated.
- Figure remains HOLD until WorldCover AOI pixels are materialized.

## F｜Water history
- No synthetic seasonal water envelope was generated.
- Figure remains HOLD until JRC GSW occurrence / seasonality pixels are materialized.

## G｜Operations conflict
- ROUTE-03 is embedded 1:1 in the left 1920×1080 region.
- Original route geometry is not scaled, smoothed, redrawn or re-authored.
- Current reported operations are added as a separate right-side evidence/consequence panel.
- Unbound program locations remain explicitly OPEN.
