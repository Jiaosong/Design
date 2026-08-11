#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/outputs"
mkdir -p "$OUT"
export QT_QPA_PLATFORM=offscreen

printf '%s\n' "SP01-R02 | GIS Reality Gate | REAL QGIS RUNTIME" | tee "$OUT/runtime_log.txt"
printf '%s\n' "Training data only. EPSG:3857 is a metric runtime placeholder, NOT a project CRS." | tee -a "$OUT/runtime_log.txt"

command -v qgis_process | tee "$OUT/qgis_process_path.txt"
qgis_process --version | tee "$OUT/qgis_version.txt"
python3 - <<'PY' | tee "$OUT/python_qgis_import.txt"
from qgis.core import Qgis
print(Qgis.QGIS_VERSION)
PY
ogr2ogr --version | tee "$OUT/gdal_version.txt"

# Convert the synthetic XY CSV into a real vector datasource with an explicit CRS.
# This closes only the software/runtime gate. It does NOT close the real-project CRS/data gate.
rm -f "$OUT/training_points.gpkg"
ogr2ogr \
  -f GPKG "$OUT/training_points.gpkg" "$ROOT/training_points.csv" \
  -oo X_POSSIBLE_NAMES=x_m \
  -oo Y_POSSIBLE_NAMES=y_m \
  -a_srs EPSG:3857 \
  -nln training_points

ogrinfo -so -al "$OUT/training_points.gpkg" | tee "$OUT/training_points_ogrinfo.txt"

ALG="qgis:heatmapkerneldensityestimation"
qgis_process help "$ALG" | tee "$OUT/qgis_heatmap_help.txt"

for radius in 75 150 300; do
  for pixel in 10 25 50; do
    out="$OUT/kde_r${radius}_p${pixel}.tif"
    rm -f "$out"
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
python3 "$ROOT/build_qgis_project.py" | tee "$OUT/build_qgis_project.log"
test -s "$OUT/SP01_R02_QGIS_Runtime.qgz"

# Analyze only the outputs that QGIS actually created.
python3 "$ROOT/analyze_qgis_outputs.py" | tee "$OUT/analysis_stdout.json"

# Fail closed unless the runtime receipt itself says PASS.
python3 - <<'PY'
from pathlib import Path
import json
root = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
# GitHub step runs with the exercise folder as cwd.
out = Path('outputs')
receipt = json.loads((out/'runtime_receipt.json').read_text())
gate = json.loads((out/'gate_decision.json').read_text())
assert receipt['qgis_runtime_gate'] == 'PASS', receipt
assert gate['runtime_gate'] == 'PASS', gate
assert gate['project_crs_gate'] == 'OPEN', gate
assert gate['project_data_gate'] == 'OPEN', gate
print(json.dumps({'runtime_gate':'PASS','project_crs_gate':'OPEN','project_data_gate':'OPEN'}, indent=2))
PY

find "$OUT" -maxdepth 1 -type f -printf '%f\t%s bytes\n' | sort | tee "$OUT/artifact_file_list.txt"
echo "SP01-R02 QGIS runtime gate completed." | tee -a "$OUT/runtime_log.txt"
