#!/usr/bin/env bash
set -euo pipefail

# OLEANDER managed Blender runtime recovery.
# Restores the canonical Blender 5.2.0 LTS runtime without vendoring the binary
# in Git. Supports either a pre-existing archive or an official Blender mirror.

version="5.2.0"
series="5.2"
archive_name="blender-${version}-linux-x64.tar.xz"
expected_sha="96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48"
runtime_root="${OLEANDER_RUNTIME_ROOT:-/mnt/data/runtime}"
runtime_home="${runtime_root}/blender-${version}-lts"
managed_bin="${runtime_home}/blender"
cache_dir="${OLEANDER_RUNTIME_CACHE:-${runtime_root}/cache}"
archive_path="${cache_dir}/${archive_name}"
source_archive=""

usage() {
  cat <<'EOF'
Usage: restore-blender.sh [--archive /path/to/blender-5.2.0-linux-x64.tar.xz] [--force]

Resolution:
  1. Existing canonical managed runtime -> probe and exit PASS.
  2. --archive PATH -> verify SHA-256, install.
  3. Cached archive in $OLEANDER_RUNTIME_CACHE -> verify, install.
  4. Official Blender mirror -> download, verify, install.

The script never treats download/install success as design or engineering PASS.
EOF
}

force=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive)
      [[ $# -ge 2 ]] || { echo "--archive requires a path" >&2; exit 2; }
      source_archive="$2"; shift 2 ;;
    --force) force=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

probe() {
  local bin="$1"
  [[ -x "$bin" ]] || return 1
  local first_line
  first_line="$($bin --version 2>/dev/null | head -1 || true)"
  [[ "$first_line" == "Blender ${version}"* ]]
}

if [[ $force -eq 0 ]] && probe "$managed_bin"; then
  printf 'OLEANDER_BLENDER_RESTORE={"status":"PASS","action":"REUSE","version":"%s","bin":"%s"}\n' "$version" "$managed_bin"
  exit 0
fi

mkdir -p "$cache_dir" "$runtime_root"

if [[ -n "$source_archive" ]]; then
  [[ -f "$source_archive" ]] || { echo "Archive not found: $source_archive" >&2; exit 3; }
  cp -f "$source_archive" "$archive_path"
elif [[ ! -f "$archive_path" ]]; then
  url="https://download.blender.org/release/Blender${series}/${archive_name}"
  echo "Downloading official Blender archive: $url" >&2
  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --retry 3 --retry-delay 2 --output "${archive_path}.partial" "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "${archive_path}.partial" "$url"
  else
    echo "No curl/wget available and no local archive supplied." >&2
    exit 4
  fi
  mv "${archive_path}.partial" "$archive_path"
fi

actual_sha="$(sha256sum "$archive_path" | awk '{print $1}')"
if [[ "$actual_sha" != "$expected_sha" ]]; then
  echo "Blender archive SHA mismatch." >&2
  echo "expected=$expected_sha" >&2
  echo "actual=$actual_sha" >&2
  exit 5
fi

tmp="${runtime_root}/.restore-blender-${version}-$$"
rm -rf "$tmp"
mkdir -p "$tmp"
tar -xf "$archive_path" -C "$tmp"
extracted="${tmp}/blender-${version}-linux-x64"
[[ -x "${extracted}/blender" ]] || { echo "Extracted Blender binary missing." >&2; exit 6; }

rm -rf "$runtime_home"
mv "$extracted" "$runtime_home"
rm -rf "$tmp"

probe "$managed_bin" || { echo "Installed Blender runtime probe failed." >&2; exit 7; }

# A global symlink is best-effort only. The canonical wrapper also resolves the
# managed runtime directly, so lack of /usr/local write permission is not fatal.
if [[ -w /usr/local/bin ]] || [[ ! -e /usr/local/bin/blender ]]; then
  ln -sfn "$managed_bin" /usr/local/bin/blender 2>/dev/null || true
  ln -sfn "$managed_bin" /usr/local/bin/oleander-blender 2>/dev/null || true
fi

printf 'OLEANDER_BLENDER_RESTORE={"status":"PASS","action":"INSTALL","version":"%s","sha256":"%s","bin":"%s"}\n' "$version" "$actual_sha" "$managed_bin"
