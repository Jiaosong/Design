#!/usr/bin/env bash
# Source this file to expose the OLEANDER shared Blender runtime.

_oleander_blender_fallback="/mnt/data/runtime/blender-5.2.0-lts/blender"

if [[ -n "${OLEANDER_BLENDER_BIN:-}" && -x "${OLEANDER_BLENDER_BIN}" ]]; then
  _oleander_resolved_blender="${OLEANDER_BLENDER_BIN}"
elif command -v blender >/dev/null 2>&1; then
  _oleander_resolved_blender="$(command -v blender)"
elif [[ -x "${_oleander_blender_fallback}" ]]; then
  _oleander_resolved_blender="${_oleander_blender_fallback}"
else
  echo "OLEANDER Blender runtime not found. Set OLEANDER_BLENDER_BIN or install Blender 5.2 LTS on PATH." >&2
  unset _oleander_blender_fallback
  return 127 2>/dev/null || exit 127
fi

export OLEANDER_BLENDER_VERSION="5.2.0 LTS"
export OLEANDER_BLENDER_BUILD="fbe6228777e7"
export OLEANDER_BLENDER_BIN="${_oleander_resolved_blender}"
export OLEANDER_BLENDER_HOME="$(cd "$(dirname "${_oleander_resolved_blender}")" && pwd)"
export OLEANDER_RENDER_ENGINE="CYCLES"

unset _oleander_resolved_blender
unset _oleander_blender_fallback
