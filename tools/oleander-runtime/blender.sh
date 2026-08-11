#!/usr/bin/env bash
set -euo pipefail

fallback="/mnt/data/runtime/blender-5.2.0-lts/blender"

if [[ -n "${OLEANDER_BLENDER_BIN:-}" && -x "${OLEANDER_BLENDER_BIN}" ]]; then
  blender_bin="${OLEANDER_BLENDER_BIN}"
elif command -v blender >/dev/null 2>&1; then
  blender_bin="$(command -v blender)"
elif [[ -x "$fallback" ]]; then
  blender_bin="$fallback"
else
  echo "OLEANDER Blender runtime not found." >&2
  echo "Set OLEANDER_BLENDER_BIN, put Blender 5.2 LTS on PATH, or materialize the managed runtime." >&2
  exit 127
fi

exec "$blender_bin" "$@"
