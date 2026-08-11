#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/toolchain.env"
DEST="$OLEANDER_COCOS_HOME"
BIN_DIR="$OLEANDER_COCOS_BIN_DIR"

mkdir -p "$DEST" "$BIN_DIR" "$OLEANDER_COCOS_PROJECT_ROOT"
cp "$SCRIPT_DIR/toolchain.env" "$DEST/toolchain.env"
cp "$SCRIPT_DIR/doctor.sh" "$DEST/doctor.sh"
chmod +x "$DEST/doctor.sh"

if ! getent hosts github.com >/dev/null 2>&1 || ! getent hosts registry.npmjs.org >/dev/null 2>&1; then
  echo "ERROR: outbound DNS/network is unavailable; cannot download upstream COCOS sources/dependencies." >&2
  exit 70
fi

current="$(node -p 'process.versions.node' 2>/dev/null || echo 0.0.0)"
if ! node -e "const a='$current'.split('.').map(Number),b='$OLEANDER_COCOS_NODE_VERSION'.split('.').map(Number);process.exit(a[0]>b[0]||a[0]===b[0]&&(a[1]>b[1]||a[1]===b[1]&&a[2]>=b[2])?0:1)"; then
  if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then
    source "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
    nvm install "$OLEANDER_COCOS_NODE_VERSION"
    nvm use "$OLEANDER_COCOS_NODE_VERSION"
  else
    echo "ERROR: Node >= $OLEANDER_COCOS_NODE_VERSION required; current=$current" >&2
    exit 65
  fi
fi

# Optional authenticated fetches. Process-local Git config avoids writing a token into repo/global config.
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  export GIT_CONFIG_COUNT=1
  export GIT_CONFIG_KEY_0="url.https://x-access-token:${GITHUB_TOKEN}@github.com/.insteadOf"
  export GIT_CONFIG_VALUE_0="https://github.com/"
fi

npm install -g node-gyp

if [[ ! -d "$DEST/cli/.git" ]]; then
  git clone https://github.com/cocos/cocos-cli.git "$DEST/cli"
fi
git -C "$DEST/cli" fetch --all --tags --force
git -C "$DEST/cli" checkout --detach "$OLEANDER_COCOS_CLI_SHA"

actual_cli="$(git -C "$DEST/cli" rev-parse HEAD)"
if [[ "$actual_cli" != "$OLEANDER_COCOS_CLI_SHA" ]]; then
  echo "ERROR: CLI SHA mismatch: expected=$OLEANDER_COCOS_CLI_SHA actual=$actual_cli" >&2
  exit 66
fi

pushd "$DEST/cli" >/dev/null
npm run init
npm install
npm run download-tools
npm run build
popd >/dev/null

ENGINE_DIR="$DEST/cli/packages/engine"
if [[ ! -d "$ENGINE_DIR/.git" ]]; then
  echo "ERROR: CLI-managed engine was not materialized at $ENGINE_DIR" >&2
  exit 67
fi
actual_engine="$(git -C "$ENGINE_DIR" rev-parse HEAD)"
if [[ "$actual_engine" != "$OLEANDER_COCOS_ENGINE_SHA" ]]; then
  echo "ERROR: Engine SHA mismatch: expected=$OLEANDER_COCOS_ENGINE_SHA actual=$actual_engine" >&2
  exit 68
fi
if [[ ! -f "$DEST/cli/dist/cli.js" ]]; then
  echo "ERROR: COCOS CLI build did not produce dist/cli.js" >&2
  exit 69
fi

install -m 0755 "$SCRIPT_DIR/bin/oleander-cocos" "$BIN_DIR/oleander-cocos"
"$BIN_DIR/oleander-cocos" doctor

echo "OLEANDER COCOS 4 shared toolchain installed: $DEST"
echo "Gateway: $BIN_DIR/oleander-cocos"
