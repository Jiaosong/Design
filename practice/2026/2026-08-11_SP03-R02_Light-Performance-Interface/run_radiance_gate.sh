#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="$ROOT/runtime"; OUT="$ROOT/outputs"
rm -rf "$RUN" "$OUT"; mkdir -p "$RUN" "$OUT"
export RAYPATH=".:/usr/share/radiance/lib:/usr/local/lib/ray"

python3 "$ROOT/generate_scene.py" | tee "$RUN/generate_scene.log"
{
  echo "rtrace=$(command -v rtrace)"; rtrace -version 2>&1 || true
  echo "rpict=$(command -v rpict)"; rpict -version 2>&1 || true
  echo "evalglare=$(command -v evalglare)"; evalglare -v 2>&1 || true
  echo "gensky=$(command -v gensky)"; gensky -version 2>&1 || true
} | tee "$RUN/radiance_versions.txt"

cat > "$RUN/sky_sources.rad" <<'RAD'
skyfunc glow sky_glow
0
0
4 1 1 1 0
sky_glow source sky
0
0
4 0 0 1 180
skyfunc glow ground_glow
0
0
4 0.2 0.2 0.2 0
ground_glow source ground
0
0
4 0 0 -1 180
RAD

declare -A SKYARGS
SKYARGS[OVC]="-ang 45 0 -c"
SKYARGS[CLEAR_E]="-ang 25 -60 +s"
SKYARGS[CLEAR_HIGH]="-ang 65 0 +s"
SKYARGS[CLEAR_W]="-ang 25 60 +s"
for sky in OVC CLEAR_E CLEAR_HIGH CLEAR_W; do
  gensky ${SKYARGS[$sky]} > "$RUN/sky_${sky}.rad"
done

for scheme in A B; do
  for sky in OVC CLEAR_E CLEAR_HIGH CLEAR_W; do
    oct="$RUN/${scheme}_${sky}.oct"
    oconv "$RUN/materials.rad" "$RUN/room_${scheme}.rad" "$RUN/sky_${sky}.rad" "$RUN/sky_sources.rad" > "$oct"
    raw="$RUN/irr_${scheme}_${sky}.txt"
    rtrace -I+ -h -ab 5 -ad 4096 -as 1024 -aa 0.10 -ar 256 -lw 1e-5 "$oct" < "$RUN/sensors.pts" > "$raw"
    python3 "$ROOT/convert_rtrace.py" --raw "$raw" --sensors "$RUN/sensors.csv" --out "$RUN/ill_${scheme}_${sky}.csv" --scheme "$scheme" --sky "$sky"
  done
done

for scheme in A B; do
  for sky in CLEAR_E CLEAR_W; do
    oct="$RUN/${scheme}_${sky}.oct"
    python3 - "$RUN/views.json" <<'PY' | while IFS='|' read -r role vp vd vu; do
import json,sys
for v in json.load(open(sys.argv[1])):
 print(v['role']+'|'+' '.join(map(str,v['vp']))+'|'+' '.join(map(str,v['vd']))+'|'+' '.join(map(str,v['vu'])))
PY
      hdr="$RUN/view_${scheme}_${sky}_${role}.hdr"
      txt="$RUN/evalglare_${scheme}_${sky}_${role}.txt"
      rpict -vta -vp $vp -vd $vd -vu $vu -vh 180 -vv 180 -x 800 -y 800 -ab 4 -ad 2048 -as 512 -aa 0.15 -ar 128 -lw 1e-4 "$oct" > "$hdr"
      evalglare -d "$hdr" > "$txt"
      python3 "$ROOT/parse_evalglare.py" --input "$txt" --out "$RUN/glare_${scheme}_${sky}_${role}.csv" --scheme "$scheme" --sky "$sky" --role "$role"
    done
  done
done

python3 "$ROOT/analyze_results.py" | tee "$OUT/analyze_stdout.json"
python3 - <<'PY'
import json
from pathlib import Path
g=json.loads(Path('outputs/gate_decision.json').read_text())
assert g['radiance_runtime_gate']=='PASS',g
assert g['glare_runtime_gate']=='PASS',g
assert g['performance_interface_gate']=='PASS',g
assert g['project_reality_promotion'] is False,g
print(json.dumps(g,indent=2))
PY
find "$RUN" "$OUT" -type f -printf '%P\t%s bytes\n' | sort > "$OUT/artifact_file_list.txt"
