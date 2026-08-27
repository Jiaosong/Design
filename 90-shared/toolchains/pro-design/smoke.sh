#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$repo_root"

export OLEANDER_PRO_RUNTIME_HOME="${OLEANDER_PRO_RUNTIME_HOME:-${RUNNER_TEMP:-/tmp}/oleander-pro-design}"
export OLEANDER_PRO_MATERIALIZE_MEDIA="${OLEANDER_PRO_MATERIALIZE_MEDIA:-1}"
smoke_dir="${OLEANDER_PRO_SMOKE_DIR:-${RUNNER_TEMP:-/tmp}/oleander-pro-smoke}"
mkdir -p "$smoke_dir"

python3 -m json.tool 00-governance/runtime/OLEANDER_PRO_DESIGN_TOOLCHAIN_RUNTIME_v0.1.json >/dev/null
for f in 90-shared/toolchains/pro-design/*.sh; do bash -n "$f"; done

bash 90-shared/toolchains/pro-design/materialize.sh
bash 90-shared/toolchains/pro-design/probe.sh

OUT="$smoke_dir/smoke.ifc" bash 90-shared/toolchains/pro-design/python.sh - <<'PY'
import os, ifcopenshell, ifcopenshell.guid
out = os.environ['OUT']
model = ifcopenshell.file(schema='IFC4')
model.create_entity('IfcProject', GlobalId=ifcopenshell.guid.new(), Name='OLEANDER_PRO_SMOKE')
model.write(out)
reopened = ifcopenshell.open(out)
projects = reopened.by_type('IfcProject')
assert len(projects) == 1 and projects[0].Name == 'OLEANDER_PRO_SMOKE'
print('IFC_CREATE_WRITE_REOPEN=PASS')
PY
test -s "$smoke_dir/smoke.ifc"

OUT="$smoke_dir/smoke.step" bash 90-shared/toolchains/pro-design/python.sh - <<'PY'
import os, cadquery as cq
out = os.environ['OUT']
solid = cq.Workplane('XY').box(20, 10, 5)
cq.exporters.export(solid, out)
reopened = cq.importers.importStep(out)
bb = reopened.val().BoundingBox()
assert abs(bb.xlen - 20) < 1e-6 and abs(bb.ylen - 10) < 1e-6 and abs(bb.zlen - 5) < 1e-6
print('STEP_EXPORT_REOPEN=PASS')
PY
test -s "$smoke_dir/smoke.step"

OUT="$smoke_dir/smoke.dxf" bash 90-shared/toolchains/pro-design/python.sh - <<'PY'
import os, ezdxf
out = os.environ['OUT']
doc = ezdxf.new('R2018')
msp = doc.modelspace()
msp.add_line((0, 0), (100, 0))
msp.add_circle((50, 25), radius=10)
doc.saveas(out)
reopened = ezdxf.readfile(out)
assert len(reopened.modelspace()) >= 2
print('DXF_CREATE_REOPEN=PASS')
PY
test -s "$smoke_dir/smoke.dxf"

png="$smoke_dir/smoke.png"
video="$smoke_dir/smoke.mkv"
bash 90-shared/toolchains/pro-design/raster.sh -size 64x64 gradient: -colorspace sRGB "$png"
test "$(bash 90-shared/toolchains/pro-design/raster.sh "$png" -format '%wx%h' info:)" = "64x64"
bash 90-shared/toolchains/pro-design/motion.sh -hide_banner -loglevel error -f lavfi -i testsrc=size=64x64:rate=5 -t 1 -c:v ffv1 -y "$video"
ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$video" | grep -q '64,64'
echo 'RASTER_AND_MOTION=PASS'

if [[ "${OLEANDER_PRO_SKIP_FREECAD:-0}" != "1" ]]; then
  export OLEANDER_PRO_MATERIALIZE_FREECAD=1
  bash 90-shared/toolchains/pro-design/materialize.sh
  bash 90-shared/toolchains/pro-design/freecad.sh --version

  cat > "$smoke_dir/freecad_smoke.py" <<'PY'
import os
import FreeCAD as App
import Part
import Path
import Path.Main.Job as PathJob
from Path.Post.Processor import PostProcessorFactory
from Machine.models.machine import Machine, Toolhead, ToolheadType

smoke_dir = os.environ['OLEANDER_PRO_SMOKE_DIR']
doc = App.newDocument('OLEANDER_PRO_SMOKE')

# Real parametric/document geometry and native FreeCAD source.
obj = doc.addObject('Part::Feature', 'Box')
obj.Shape = Part.makeBox(20, 10, 5)
doc.recompute()
fcstd = os.path.join(smoke_dir, 'freecad-smoke.FCStd')
step = os.path.join(smoke_dir, 'freecad-smoke.step')
Part.export([obj], step)

# Build a real CAM Job and a real Path feature. We intentionally do not invoke
# the GUI-context-dependent Path.Op.* factory here; headless 1.1.3 currently
# has a known upstream controller-selection bug in those factories.
job = PathJob.Create('Job', [obj], None)
doc.recompute()
assert job is not None and job.Operations is not None and job.Tools is not None
assert len(job.Tools.Group) >= 1

tc = job.Tools.Group[0]
op = doc.addObject('Path::Feature', 'OLEANDER_Smoke_Toolpath')
op.Label = 'OLEANDER Smoke Toolpath'
if not hasattr(op, 'ToolController'):
    op.addProperty('App::PropertyLink', 'ToolController', 'Path')
op.ToolController = tc
if not hasattr(op, 'Active'):
    op.addProperty('App::PropertyBool', 'Active', 'Path')
op.Active = True
op.Path = Path.Path([
    Path.Command('G0', {'X': 0.0, 'Y': 0.0, 'Z': 5.0}),
    Path.Command('G1', {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'F': 100.0}),
    Path.Command('G1', {'X': 10.0, 'Y': 0.0, 'Z': 0.0, 'F': 100.0}),
    Path.Command('G1', {'X': 10.0, 'Y': 10.0, 'Z': 0.0, 'F': 100.0}),
    Path.Command('G0', {'Z': 5.0}),
])
job.Proxy.addOperation(op)
doc.recompute()
assert op in job.Operations.Group
assert len(op.Path.Commands) >= 5

# Explicit controller dialect: LinuxCNC. FreeCAD's own CAM tests exercise
# PostProcessorFactory + export2(), so this follows the native postprocess path.
job.PostProcessor = 'linuxcnc'
post = PostProcessorFactory.get_post_processor(job, 'linuxcnc')
assert post is not None
machine = Machine.create_3axis_config()
machine.name = 'OLEANDER Smoke 3-axis'
machine.toolheads = [
    Toolhead(
        name='OLEANDER Smoke Spindle',
        toolhead_type=ToolheadType.ROTARY,
        min_rpm=0,
        max_rpm=24000,
        max_power_kw=1.0,
    )
]
post._machine = machine
post.apply_configuration_bundle()
outputs = post.export2()
assert outputs and isinstance(outputs[0], tuple) and len(outputs[0]) >= 2
gcode = '\n'.join(str(item[1]) for item in outputs if len(item) >= 2 and item[1])
assert gcode.strip()
assert 'G21' in gcode, gcode
assert 'G0' in gcode, gcode
assert 'G1' in gcode, gcode

gcode_path = os.path.join(smoke_dir, 'freecad-smoke-linuxcnc.ngc')
with open(gcode_path, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(gcode)
assert os.path.getsize(gcode_path) > 0

doc.recompute()
doc.saveAs(fcstd)
assert os.path.getsize(fcstd) > 0 and os.path.getsize(step) > 0
print('FREECAD_PARAMETRIC_STEP_EXPORT=PASS')
print('FREECAD_CAM_JOB_PATH_OBJECT=PASS')
print('FREECAD_LINUXCNC_POSTPROCESS_GCODE=PASS')
print('FREECAD_CAM_MACHINE_SAFETY=NOT_PROVEN_BY_SMOKE')
PY
  export OLEANDER_PRO_SMOKE_DIR="$smoke_dir"
  export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
  bash 90-shared/toolchains/pro-design/freecad.sh "$smoke_dir/freecad_smoke.py"
  test -s "$smoke_dir/freecad-smoke.FCStd"
  test -s "$smoke_dir/freecad-smoke.step"
  test -s "$smoke_dir/freecad-smoke-linuxcnc.ngc"
  grep -q 'G21' "$smoke_dir/freecad-smoke-linuxcnc.ngc"
  grep -q 'G0' "$smoke_dir/freecad-smoke-linuxcnc.ngc"
  grep -q 'G1' "$smoke_dir/freecad-smoke-linuxcnc.ngc"
fi

echo 'OLEANDER_PRO_DESIGN_TOOLCHAIN_SMOKE=PASS'
