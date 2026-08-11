#!/usr/bin/env bash
set -euo pipefail

SOURCE="${1:-$(pwd)/05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source}"
DEST="${2:-$(pwd)/05-cases/c04-qingjiang-stone-book/game-ui/cocos4-project}"

if ! command -v oleander-cocos >/dev/null 2>&1; then
  echo "ERROR: oleander-cocos gateway missing" >&2
  exit 69
fi

if [[ ! -d "$SOURCE/assets" ]]; then
  echo "ERROR: authoritative source assets missing: $SOURCE/assets" >&2
  exit 66
fi

# The pinned COCOS CLI refuses to create a project when the target path already
# exists, even when it is empty. Fail on non-empty targets; remove only an empty
# placeholder directory before invoking the official create command.
if [[ -e "$DEST" ]]; then
  if [[ -n "$(ls -A "$DEST" 2>/dev/null || true)" ]]; then
    echo "ERROR: destination is not empty: $DEST" >&2
    exit 73
  fi
  rmdir "$DEST"
fi

oleander-cocos create "$DEST" 2d

# Fail closed if the official create command did not materialize the expected
# governed project metadata before project source is overlaid.
[[ -f "$DEST/package.json" ]] || { echo "ERROR: COCOS project package.json missing after create" >&2; exit 65; }
[[ -f "$DEST/settings/v2/packages/engine.json" ]] || { echo "ERROR: COCOS engine settings missing after create" >&2; exit 65; }

mkdir -p "$DEST/assets"
cp -R "$SOURCE/assets/." "$DEST/assets/"

# Validate the minimum C04 source contract without calling upstream commands
# that are not registered by the pinned CLI commit (notably import/info).
[[ -f "$DEST/assets/data/chapters.json" ]] || { echo "ERROR: chapters.json missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/data/nodes.json" ]] || { echo "ERROR: nodes.json missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/scripts/core/AppState.ts" ]] || { echo "ERROR: AppState.ts missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/scripts/core/NodeRegistry.ts" ]] || { echo "ERROR: NodeRegistry.ts missing after source overlay" >&2; exit 65; }

node - "$DEST/package.json" <<'NODE'
const fs = require('fs');
const file = process.argv[2];
const pkg = JSON.parse(fs.readFileSync(file, 'utf8'));
if (pkg.type !== '2d') {
  console.error(`ERROR: materialized project type is ${pkg.type}; expected 2d`);
  process.exit(65);
}
if (!pkg.creator || pkg.creator.version !== '4.0.0') {
  console.error('ERROR: materialized project creator metadata is not COCOS 4.0.0');
  process.exit(65);
}
NODE

echo "C04 materialized as a real COCOS CLI project at: $DEST"
