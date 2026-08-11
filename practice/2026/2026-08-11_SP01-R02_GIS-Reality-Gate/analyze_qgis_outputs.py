from pathlib import Path
import csv, json, math, os
from osgeo import gdal, osr
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
RADII = (75, 150, 300)
PIXELS = (10, 25, 50)
STUDY = (0.0, 1000.0, 0.0, 1000.0)  # xmin,xmax,ymin,ymax; training-only local metric box


def components(mask):
    mask = np.asarray(mask, dtype=bool)
    seen = np.zeros(mask.shape, dtype=bool)
    n = 0
    h, w = mask.shape
    for r in range(h):
        for c in range(w):
            if not mask[r, c] or seen[r, c]:
                continue
            n += 1
            stack = [(r, c)]
            seen[r, c] = True
            while stack:
                rr, cc = stack.pop()
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and mask[nr, nc] and not seen[nr, nc]:
                            seen[nr, nc] = True
                            stack.append((nr, nc))
    return n


def raster_metrics(path, radius, pixel):
    ds = gdal.Open(str(path))
    if ds is None:
        raise RuntimeError(f"Cannot open {path}")
    gt = ds.GetGeoTransform()
    proj = ds.GetProjection()
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(float)
    nodata = band.GetNoDataValue()
    valid = np.isfinite(arr)
    if nodata is not None:
        valid &= arr != nodata
    values = np.where(valid, arr, 0.0)

    px = abs(float(gt[1]))
    py = abs(float(gt[5]))
    if not (math.isclose(px, pixel, rel_tol=0, abs_tol=1e-6) and math.isclose(py, pixel, rel_tol=0, abs_tol=1e-6)):
        raise RuntimeError(f"Pixel size mismatch for {path.name}: got {px},{py}, expected {pixel}")

    x_centers = gt[0] + (np.arange(ds.RasterXSize) + 0.5) * gt[1]
    y_centers = gt[3] + (np.arange(ds.RasterYSize) + 0.5) * gt[5]
    X, Y = np.meshgrid(x_centers, y_centers)
    xmin, xmax, ymin, ymax = STUDY
    study_mask = valid & (X >= xmin) & (X <= xmax) & (Y >= ymin) & (Y <= ymax)

    full_sum = float(values[valid].sum())
    inside_sum = float(values[study_mask].sum())
    spill_fraction = None if full_sum == 0 else float(max(0.0, 1.0 - inside_sum / full_sum))
    maxv = float(values[valid].max()) if np.any(valid) else 0.0
    norm = np.zeros_like(values)
    if maxv > 0:
        norm = values / maxv
    t50 = study_mask & (norm >= 0.50)
    t75 = study_mask & (norm >= 0.75)
    area50 = float(t50.sum() * px * py)
    area75 = float(t75.sum() * px * py)
    c50 = int(components(t50))

    weights = np.where(study_mask, values, 0.0)
    wsum = float(weights.sum())
    if wsum > 0:
        cx = float((weights * X).sum() / wsum)
        cy = float((weights * Y).sum() / wsum)
    else:
        cx = cy = None

    sr = osr.SpatialReference()
    sr.ImportFromWkt(proj)
    authority = None
    if sr:
        name = sr.GetAuthorityName(None)
        code = sr.GetAuthorityCode(None)
        if name and code:
            authority = f"{name}:{code}"

    x0, y0 = gt[0], gt[3]
    x1 = gt[0] + ds.RasterXSize * gt[1]
    y1 = gt[3] + ds.RasterYSize * gt[5]

    return {
        "radius_m": radius,
        "pixel_m": pixel,
        "width_px": ds.RasterXSize,
        "height_px": ds.RasterYSize,
        "crs_authority": authority,
        "extent_xmin": min(x0, x1),
        "extent_xmax": max(x0, x1),
        "extent_ymin": min(y0, y1),
        "extent_ymax": max(y0, y1),
        "max_raw": maxv,
        "sum_raw": full_sum,
        "inside_sum_raw": inside_sum,
        "integral_proxy_full": full_sum * px * py,
        "integral_proxy_inside": inside_sum * px * py,
        "spill_fraction_outside_study": spill_fraction,
        "area_ge_50pct_max_m2": area50,
        "area_ge_75pct_max_m2": area75,
        "components_ge_50pct_max": c50,
        "weighted_centroid_x_m": cx,
        "weighted_centroid_y_m": cy,
    }


rows = []
for r in RADII:
    for p in PIXELS:
        rows.append(raster_metrics(OUT / f"kde_r{r}_p{p}.tif", r, p))

with (OUT / "sensitivity_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

summary = []
for r in RADII:
    rr = [x for x in rows if x["radius_m"] == r]
    comp_set = sorted(set(x["components_ge_50pct_max"] for x in rr))
    cxy = [(x["weighted_centroid_x_m"], x["weighted_centroid_y_m"]) for x in rr]
    shifts = []
    for i in range(len(cxy)):
        for j in range(i+1, len(cxy)):
            if None not in cxy[i] + cxy[j]:
                shifts.append(math.hypot(cxy[i][0]-cxy[j][0], cxy[i][1]-cxy[j][1]))
    areas = [x["area_ge_50pct_max_m2"] for x in rr]
    ints = [x["integral_proxy_inside"] for x in rr]
    def rel_spread(vals):
        med = float(np.median(vals))
        return None if med == 0 else (max(vals)-min(vals))/med
    summary.append({
        "radius_m": r,
        "component_counts_50pct": comp_set,
        "max_weighted_centroid_shift_m": max(shifts) if shifts else 0.0,
        "area50_relative_spread": rel_spread(areas),
        "integral_inside_relative_spread": rel_spread(ints),
        "exercise_heuristic_only": "stable" if len(comp_set)==1 and (max(shifts) if shifts else 0.0) <= 50 and (rel_spread(areas) or 0) <= 0.15 else "resolution-sensitive",
    })

runtime_version = (OUT / "qgis_version.txt").read_text(encoding="utf-8", errors="ignore").strip() if (OUT / "qgis_version.txt").exists() else ""
qgz_ok = (OUT / "SP01_R02_QGIS_Runtime.qgz").exists() and (OUT / "SP01_R02_QGIS_Runtime.qgz").stat().st_size > 0
all_crs = all(x["crs_authority"] == "EPSG:3857" for x in rows)
all_outputs = all((OUT / f"kde_r{r}_p{p}.tif").exists() for r in RADII for p in PIXELS)

receipt = {
    "exercise":"SP01-R02 GIS Reality Gate",
    "truth_state":"QGIS runtime executed on synthetic training data",
    "qgis_version":runtime_version,
    "algorithm":"qgis:heatmapkerneldensityestimation",
    "kernel":"Quartic (KERNEL=0)",
    "output_value":"Raw (OUTPUT_VALUE=0)",
    "radii_m":list(RADII),
    "pixel_sizes_m":list(PIXELS),
    "training_crs":"EPSG:3857 placeholder for runtime-only metric coordinates",
    "project_crs_gate":"OPEN — no real site/projected CRS selected",
    "project_data_gate":"OPEN — bundled 24 points are synthetic",
    "qgis_runtime_gate":"PASS" if runtime_version and all_outputs and all_crs and qgz_ok else "FAIL",
    "pixel_sensitivity":"OBSERVED — metrics recorded; heuristic is exercise-only, not a project criterion",
    "edge_effect":"OBSERVED — spill beyond 0–1000 m study box recorded; no project correction rule promoted",
    "qgz_project_created":qgz_ok,
}
(OUT / "runtime_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
(OUT / "pixel_sensitivity_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

edge_rows = [{
    "radius_m":x["radius_m"],
    "pixel_m":x["pixel_m"],
    "spill_fraction_outside_study":x["spill_fraction_outside_study"],
    "note":"Boundary mass spill relative to exercise study box; not a corrected edge-bias estimate."
} for x in rows]
with (OUT / "edge_effect_metrics.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(edge_rows[0].keys()))
    w.writeheader(); w.writerows(edge_rows)

project_gate_closed = False
gate = {
    "runtime_gate":"PASS" if receipt["qgis_runtime_gate"]=="PASS" else "FAIL",
    "software_reality":"VERIFIED" if receipt["qgis_runtime_gate"]=="PASS" else "BLOCKED",
    "project_crs_gate":"OPEN",
    "project_data_gate":"OPEN",
    "project_candidate_promotion":False,
    "practice_status":"QGIS RUNTIME VERIFIED / PROJECT REALITY OPEN" if receipt["qgis_runtime_gate"]=="PASS" else "QGIS RUNTIME BLOCKED",
    "reason":"Actual QGIS Processing outputs exist, but EPSG:3857 and all point coordinates remain exercise-only placeholders; no real project evidence is present."
}
(OUT / "gate_decision.json").write_text(json.dumps(gate, indent=2, ensure_ascii=False), encoding="utf-8")

print(json.dumps({"receipt":receipt,"sensitivity":summary,"gate":gate}, indent=2, ensure_ascii=False))
