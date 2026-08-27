#!/usr/bin/env bash
set -euo pipefail
runtime_home="${OLEANDER_PRO_RUNTIME_HOME:-/mnt/data/runtime/oleander-pro-design}"
py="${OLEANDER_PRO_PYTHON:-$runtime_home/venv/bin/python}"

python_state="UNAVAILABLE"
if [[ -x "$py" ]]; then
  if "$py" - <<'PY' >/tmp/oleander-pro-python-probe.txt 2>/dev/null
import ifcopenshell, cadquery, ezdxf
print('ifcopenshell=' + str(ifcopenshell.version))
print('cadquery=' + str(cadquery.__version__))
print('ezdxf=' + str(ezdxf.__version__))
PY
  then python_state="AVAILABLE"; fi
fi

freecad_state="UNAVAILABLE"
managed_cmd_file="$runtime_home/freecad-1.1.3/FREECAD_CMD_PATH"
managed_cmd=""
if [[ -f "$managed_cmd_file" ]]; then
  managed_cmd="$(cat "$managed_cmd_file")"
fi
if [[ -n "${OLEANDER_FREECAD_BIN:-}" && -x "${OLEANDER_FREECAD_BIN}" ]]; then
  freecad_state="AVAILABLE_ENV"
elif command -v FreeCADCmd >/dev/null 2>&1 || command -v freecadcmd >/dev/null 2>&1; then
  freecad_state="AVAILABLE_PATH"
elif [[ -n "$managed_cmd" && -x "$managed_cmd" ]]; then
  freecad_state="AVAILABLE_MANAGED_CLI"
elif [[ -x "$runtime_home/freecad-1.1.3/appdir/usr/bin/FreeCADCmd" ]]; then
  freecad_state="AVAILABLE_MANAGED_CLI"
fi

magick_state="UNAVAILABLE"
if [[ -n "${OLEANDER_MAGICK_BIN:-}" && -x "${OLEANDER_MAGICK_BIN}" ]] || command -v magick >/dev/null 2>&1 || command -v convert >/dev/null 2>&1; then
  magick_state="AVAILABLE"
fi

ffmpeg_state="UNAVAILABLE"
if [[ -n "${OLEANDER_FFMPEG_BIN:-}" && -x "${OLEANDER_FFMPEG_BIN}" ]] || command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg_state="AVAILABLE"
fi

printf '{\n'
printf '  "managed_python": "%s",\n' "$python_state"
printf '  "freecad": "%s",\n' "$freecad_state"
printf '  "imagemagick": "%s",\n' "$magick_state"
printf '  "ffmpeg": "%s"\n' "$ffmpeg_state"
printf '}\n'

if [[ "$python_state" == "AVAILABLE" ]]; then
  cat /tmp/oleander-pro-python-probe.txt >&2
fi
