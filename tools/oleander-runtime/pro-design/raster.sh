#!/usr/bin/env bash
set -euo pipefail
if [[ -n "${OLEANDER_MAGICK_BIN:-}" && -x "${OLEANDER_MAGICK_BIN}" ]]; then
  magick_bin="${OLEANDER_MAGICK_BIN}"
elif command -v magick >/dev/null 2>&1; then
  magick_bin="$(command -v magick)"
elif command -v convert >/dev/null 2>&1; then
  magick_bin="$(command -v convert)"
else
  echo "OLEANDER raster runtime not found: ImageMagick is required for this wrapper." >&2
  exit 127
fi
exec "$magick_bin" "$@"
