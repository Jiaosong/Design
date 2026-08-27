#!/usr/bin/env bash
set -euo pipefail
runtime_home="${OLEANDER_PRO_RUNTIME_HOME:-/mnt/data/runtime/oleander-pro-design}"
managed="$runtime_home/freecad-1.1.3/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"

# OLEANDER invokes FreeCAD as a non-interactive shared runtime. Prevent the
# AppImage/Qt bootstrap from attempting an X11/xcb display on headless runners.
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"

if [[ -n "${OLEANDER_FREECAD_BIN:-}" && -x "${OLEANDER_FREECAD_BIN}" ]]; then
  freecad_bin="${OLEANDER_FREECAD_BIN}"
  exec "$freecad_bin" "$@"
elif command -v FreeCADCmd >/dev/null 2>&1; then
  exec "$(command -v FreeCADCmd)" "$@"
elif command -v freecadcmd >/dev/null 2>&1; then
  exec "$(command -v freecadcmd)" "$@"
elif [[ -x "$managed" ]]; then
  export APPIMAGE_EXTRACT_AND_RUN=1
  exec "$managed" --console "$@"
else
  echo "OLEANDER FreeCAD runtime not found." >&2
  echo "Set OLEANDER_FREECAD_BIN, put FreeCADCmd on PATH, or materialize FreeCAD with OLEANDER_PRO_MATERIALIZE_FREECAD=1." >&2
  exit 127
fi
