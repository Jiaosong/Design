#!/usr/bin/env bash
set -euo pipefail
runtime_home="${OLEANDER_PRO_RUNTIME_HOME:-/mnt/data/runtime/oleander-pro-design}"
freecad_dir="$runtime_home/freecad-1.1.3"
managed_cmd_file="$freecad_dir/FREECAD_CMD_PATH"
managed_appdir="$freecad_dir/appdir"

export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"

run_freecad_cmd() {
  local bin="$1"
  shift
  local appdir=""
  case "$bin" in
    "$managed_appdir"/*) appdir="$managed_appdir" ;;
  esac
  if [[ -n "$appdir" ]]; then
    export APPDIR="$appdir"
    export PATH="$appdir/usr/bin:$appdir/bin:$PATH"
    export LD_LIBRARY_PATH="$appdir/usr/lib:$appdir/usr/lib/x86_64-linux-gnu:$appdir/lib:${LD_LIBRARY_PATH:-}"
    export QT_PLUGIN_PATH="$appdir/usr/plugins:$appdir/usr/lib/qt6/plugins:${QT_PLUGIN_PATH:-}"
  fi
  exec "$bin" "$@"
}

if [[ -n "${OLEANDER_FREECAD_BIN:-}" && -x "${OLEANDER_FREECAD_BIN}" ]]; then
  run_freecad_cmd "${OLEANDER_FREECAD_BIN}" "$@"
elif command -v FreeCADCmd >/dev/null 2>&1; then
  run_freecad_cmd "$(command -v FreeCADCmd)" "$@"
elif command -v freecadcmd >/dev/null 2>&1; then
  run_freecad_cmd "$(command -v freecadcmd)" "$@"
elif [[ -f "$managed_cmd_file" ]]; then
  managed_cmd="$(cat "$managed_cmd_file")"
  if [[ -x "$managed_cmd" ]]; then
    run_freecad_cmd "$managed_cmd" "$@"
  fi
  echo "Managed FreeCAD CLI pointer is stale or non-executable: $managed_cmd" >&2
  exit 127
elif [[ -x "$managed_appdir/usr/bin/FreeCADCmd" ]]; then
  run_freecad_cmd "$managed_appdir/usr/bin/FreeCADCmd" "$@"
else
  echo "OLEANDER FreeCAD CLI runtime not found." >&2
  echo "Set OLEANDER_FREECAD_BIN, put FreeCADCmd on PATH, or materialize the verified AppImage with OLEANDER_PRO_MATERIALIZE_FREECAD=1." >&2
  exit 127
fi
