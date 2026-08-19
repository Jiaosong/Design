#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/outputs"
rm -rf "$OUT"
mkdir -p "$OUT"
export QT_QPA_PLATFORM=offscreen

printf '%s\n' "SP01-R02 | GIS Reality Gate | REAL QGIS RUNTIME" | tee "$OUT/runtime_log.txt"
printf '%s\n' "Training data only. EPSG:3857 is a metric runtime placeholder, NOT a project CRS." | tee -a "$OUT/runtime_log.txt"

command -v qgis_process | tee "$OUT/qgis_process_path.txt"
qgis_process --version | tee "$OUT/qgis_version.txt"
/usr/bin/python3 - <<'PY' | tee "$OUT/python_qgis_import.txt"
from qgis.core import Qgis
print(Qgis.QGIS_VERSION)
PY
ogr2ogr --version | tee "$OUT/gdal_version.txt"

# Convert synthetic XY CSV to a typed GPKG. AUTODETECT_TYPE prevents the weight field
# from silently remaining String. The CRS remains a runtime-only placeholder.
ogr2ogr \
  -f GPKG "$OUT/training_points.gpkg" "$ROOT/training_points.csv" \
  -oo AUTODETECT_TYPE=YES \
  -oo X_POSSIBLE_NAMES=x_m \
  -oo Y_POSSIBLE_NAMES=y_m \
  -a_srs EPSG:3857 \
  -nln training_points

ogrinfo -so -al "$OUT/training_points.gpkg" | tee "$OUT/training_points_ogrinfo.txt"
if ! grep -Eq 'weight: (Integer|Integer64|Real)' "$OUT/training_points_ogrinfo.txt"; then
  echo "FAIL: weight field is not numeric" >&2
  exit 21
fi
printf '%s\n' '{"weight_field_numeric":true,"expected_feature_count":24}' > "$OUT/vector_schema_gate.json"

ALG="qgis:heatmapkerneldensityestimation"
qgis_process help "$ALG" | tee "$OUT/qgis_heatmap_help.txt"

for radius in 75 150 300; do
  for pixel in 10 25 50; do
    out="$OUT/kde_r${radius}_p${pixel}.tif"
    echo "RUN radius=${radius}m pixel=${pixel}m" | tee -a "$OUT/runtime_log.txt"
    qgis_process run "$ALG" -- \
      INPUT="$OUT/training_points.gpkg|layername=training_points" \
      RADIUS="$radius" \
      PIXEL_SIZE="$pixel" \
      WEIGHT_FIELD=weight \
      KERNEL=0 \
      DECAY=0 \
      OUTPUT_VALUE=0 \
      OUTPUT="$out" | tee "$OUT/qgis_r${radius}_p${pixel}.json"
    test -s "$out"
    gdalinfo -json "$out" > "$OUT/gdalinfo_r${radius}_p${pixel}.json"
  done
done

# Build a native QGIS project via the actual PyQGIS runtime.
/usr/bin/python3 "$ROOT/build_qgis_project.py" | tee "$OUT/build_qgis_project.log"
test -s "$OUT/SP01_R02_QGIS_Runtime.qgz"

# Analyze only outputs QGIS actually created.
/usr/bin/python3 "$ROOT/analyze_qgis_outputs.py" | tee "$OUT/analysis_stdout.json"

# Export three final A3 review maps through QGIS Layout itself.
/usr/bin/python3 "$ROOT/render_qgis_layouts.py" | tee "$OUT/qgis_layout_export.log"
for radius in 75 150 300; do
  test -s "$OUT/QGIS_LAYOUT_r${radius}_p25.png"
done

# Fail closed unless software runtime passes while real-project gates remain open.
/usr/bin/python3 - <<'PY'
from pathlib import Path
import json
out = Path('outputs')
receipt = json.loads((out/'runtime_receipt.json').read_text())
gate = json.loads((out/'gate_decision.json').read_text())
schema = json.loads((out/'vector_schema_gate.json').read_text())
layouts = json.loads((out/'qgis_layout_manifest.json').read_text())
assert receipt['qgis_runtime_gate'] == 'PASS', receipt
assert gate['runtime_gate'] == 'PASS', gate
assert gate['project_crs_gate'] == 'OPEN', gate
assert gate['project_data_gate'] == 'OPEN', gate
assert gate['project_candidate_promotion'] is False, gate
assert schema['weight_field_numeric'] is True, schema
assert len(layouts) == 3, layouts
print(json.dumps({
    'runtime_gate':'PASS',
    'weight_field_numeric':True,
    'qgis_layouts':3,
    'project_crs_gate':'OPEN',
    'project_data_gate':'OPEN'
}, indent=2))
PY

# Build the file listing through a temporary file so the list does not report itself as zero bytes.
find "$OUT" -maxdepth 1 -type f ! -name artifact_file_list.txt -printf '%f\t%s bytes\n' | sort > "$OUT/artifact_file_list.tmp"
mv "$OUT/artifact_file_list.tmp" "$OUT/artifact_file_list.txt"
cat "$OUT/artifact_file_list.txt"
echo "SP01-R02 QGIS runtime gate completed." | tee -a "$OUT/runtime_log.txt"

# TEMP EXECUTION ADAPTER / DO NOT MERGE.
# Reuse the already-proven QGIS/GDAL runner to materialize real C04 CH02 terrain bytes.
bash "$ROOT/run_c04_ch02_dem_materialization.sh" | tee "$OUT/c04_ch02_materialization.log"
