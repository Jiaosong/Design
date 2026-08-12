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

# Optional C04 visual-media materialization. The source authority stays text-only:
# project-approved official media are fetched into the generated Creator project,
# then pinned by SHA-256 so a changed upstream byte stream fails closed. The
# runtime never depends on the remote URL after build.
MEDIA_MANIFEST="$DEST/assets/resources/c04/ws07a/visual-media-manifest.json"
if [[ -f "$MEDIA_MANIFEST" ]]; then
  node - "$DEST" "$MEDIA_MANIFEST" <<'NODE'
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const project = path.resolve(process.argv[2]);
const manifestFile = path.resolve(process.argv[3]);
const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
const assets = Array.isArray(manifest.assets) ? manifest.assets : [];

async function main() {
  for (const asset of assets) {
    if (!asset?.sourceUrl || !asset?.sha256 || !asset?.materializedFile) {
      throw new Error(`visual media manifest asset is incomplete: ${JSON.stringify(asset)}`);
    }
    if (asset.usageGate !== 'RESEARCH_PROTOTYPE_ONLY' && asset.rightsGate !== 'PASS_PROJECT_USE_APPROVED') {
      throw new Error(`visual media asset is not approved for materialization: ${asset.assetId}`);
    }
    const response = await fetch(asset.sourceUrl, {
      headers: { 'user-agent': 'OLEANDER-C04-Media-Materializer/0.1' },
      redirect: 'follow',
    });
    if (!response.ok) throw new Error(`download ${asset.assetId} failed: HTTP ${response.status}`);
    const data = Buffer.from(await response.arrayBuffer());
    const sha = crypto.createHash('sha256').update(data).digest('hex');
    if (sha !== asset.sha256) {
      throw new Error(`SHA256 mismatch for ${asset.assetId}: expected ${asset.sha256}, got ${sha}`);
    }
    if (Number.isInteger(asset.expectedBytes) && data.length !== asset.expectedBytes) {
      throw new Error(`byte-size mismatch for ${asset.assetId}: expected ${asset.expectedBytes}, got ${data.length}`);
    }
    const out = path.resolve(project, asset.materializedFile);
    if (!out.startsWith(`${project}${path.sep}`)) throw new Error(`materializedFile escapes project: ${asset.materializedFile}`);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, data);
    console.log(`C04 visual media materialized: ${asset.assetId} -> ${path.relative(project, out)} sha256=${sha}`);
  }
}

main().catch((error) => {
  console.error(`ERROR: C04 visual media materialization failed: ${error.message}`);
  process.exit(65);
});
NODE
fi

# Validate the minimum C04 source contract without calling upstream commands
# that are not registered by the pinned CLI commit (notably import/info).
[[ -f "$DEST/assets/data/chapters.json" ]] || { echo "ERROR: chapters.json missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/data/nodes.json" ]] || { echo "ERROR: nodes.json missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/scripts/core/AppState.ts" ]] || { echo "ERROR: AppState.ts missing after source overlay" >&2; exit 65; }
[[ -f "$DEST/assets/scripts/core/NodeRegistry.ts" ]] || { echo "ERROR: NodeRegistry.ts missing after source overlay" >&2; exit 65; }

# A COCOS web build requires at least one real SceneAsset. The pinned CLI's
# `create 2d` command materializes project metadata but does not create a scene,
# so source packs must provide one explicitly. Fail here with a precise contract
# error instead of surfacing the builder's generic BUILD_FAILED (exit 34).
SCENE_FILE="$(find "$DEST/assets" -type f -name '*.scene' -print -quit)"
[[ -n "$SCENE_FILE" ]] || { echo "ERROR: no .scene asset found after source overlay; at least one COCOS SceneAsset is required" >&2; exit 65; }

node - "$SCENE_FILE" <<'NODE'
const fs = require('fs');
const file = process.argv[2];
let document;
try {
  document = JSON.parse(fs.readFileSync(file, 'utf8'));
} catch (error) {
  console.error(`ERROR: scene is not valid JSON: ${file}`);
  console.error(error.message);
  process.exit(65);
}
if (!Array.isArray(document) || !document.some((entry) => entry && entry.__type__ === 'cc.SceneAsset')) {
  console.error(`ERROR: scene does not contain a cc.SceneAsset root: ${file}`);
  process.exit(65);
}
NODE

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

echo "C04 materialized with buildable scene: ${SCENE_FILE#$DEST/}"
echo "C04 materialized as a real COCOS CLI project at: $DEST"
