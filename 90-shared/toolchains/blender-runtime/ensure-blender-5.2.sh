#!/usr/bin/env bash
set -euo pipefail

VERSION="5.2.0"
BUILD_LABEL="5.2.0 LTS"
ARCHIVE_NAME="blender-${VERSION}-linux-x64.tar.xz"
ARCHIVE_SHA256="96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48"
OFFICIAL_URL="https://download.blender.org/release/Blender5.2/${ARCHIVE_NAME}"

probe_bin() {
  local candidate="${1:-}"
  [[ -n "$candidate" && -x "$candidate" ]] || return 1
  "$candidate" --version 2>/dev/null | head -n 1 | grep -Fq "Blender ${VERSION}" || return 1
  printf '%s\n' "$candidate"
}

if probe_bin "${OLEANDER_BLENDER_BIN:-}"; then exit 0; fi
if command -v blender >/dev/null 2>&1 && probe_bin "$(command -v blender)"; then exit 0; fi
if probe_bin "/mnt/data/runtime/blender-5.2.0-lts/blender"; then exit 0; fi

if mkdir -p /mnt/data/runtime/blender-5.2.0-lts 2>/dev/null && [[ -w /mnt/data/runtime/blender-5.2.0-lts ]]; then
  TARGET_HOME="/mnt/data/runtime/blender-5.2.0-lts"
else
  TARGET_HOME="${RUNNER_TEMP:-/tmp}/oleander/blender-5.2.0-lts"
  mkdir -p "$TARGET_HOME"
fi
TARGET_BIN="$TARGET_HOME/blender"

ARCHIVE=""
for candidate in \
  "${OLEANDER_BLENDER_ARCHIVE:-}" \
  "/mnt/data/runtime/cache/${ARCHIVE_NAME}" \
  "${RUNNER_TEMP:-/tmp}/${ARCHIVE_NAME}" \
  "${HOME:-/tmp}/.cache/oleander/${ARCHIVE_NAME}"; do
  if [[ -n "$candidate" && -f "$candidate" ]]; then
    ARCHIVE="$candidate"
    break
  fi
done

if [[ -z "$ARCHIVE" ]]; then
  CACHE_DIR="${RUNNER_TEMP:-/tmp}/oleander-downloads"
  mkdir -p "$CACHE_DIR"
  ARCHIVE="$CACHE_DIR/$ARCHIVE_NAME"
  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --retry 3 --retry-delay 2 "$OFFICIAL_URL" --output "$ARCHIVE"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARCHIVE" "$OFFICIAL_URL"
  else
    echo "OLEANDER Blender recovery failed: neither curl nor wget is available." >&2
    exit 127
  fi
fi

ACTUAL_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$ARCHIVE_SHA256" ]]; then
  echo "OLEANDER Blender recovery SHA mismatch." >&2
  echo "Expected: $ARCHIVE_SHA256" >&2
  echo "Actual:   $ACTUAL_SHA" >&2
  exit 65
fi

TMP_EXTRACT="${TARGET_HOME}.extract.$$"
rm -rf "$TMP_EXTRACT"
mkdir -p "$TMP_EXTRACT"
tar -xJf "$ARCHIVE" -C "$TMP_EXTRACT" --strip-components=1

if [[ ! -x "$TMP_EXTRACT/blender" ]]; then
  echo "OLEANDER Blender recovery failed: archive extracted without blender executable." >&2
  exit 66
fi

rm -rf "$TARGET_HOME"
mv "$TMP_EXTRACT" "$TARGET_HOME"

if ! probe_bin "$TARGET_BIN" >/dev/null; then
  echo "OLEANDER Blender recovery failed version probe for $BUILD_LABEL." >&2
  exit 67
fi

printf '%s\n' "$TARGET_BIN"
