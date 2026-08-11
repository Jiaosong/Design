#!/usr/bin/env bash
set -euo pipefail
DEST="${OLEANDER_COCOS_HOME:-/opt/oleander/cocos4}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/toolchain.env"
mkdir -p "$DEST" "$OLEANDER_COCOS_PROJECT_ROOT"
cp "$SCRIPT_DIR/toolchain.env" "$DEST/toolchain.env"
cp "$SCRIPT_DIR/doctor.sh" "$DEST/doctor.sh"
chmod +x "$DEST/doctor.sh"
if ! getent hosts github.com >/dev/null 2>&1 || ! getent hosts registry.npmjs.org >/dev/null 2>&1; then echo "ERROR: outbound DNS/network is unavailable; cannot download upstream COCOS sources/dependencies." >&2; exit 70; fi
current="$(node -p 'process.versions.node' 2>/dev/null || echo 0.0.0)"
if ! node -e "const a='$current'.split('.').map(Number),b='$OLEANDER_COCOS_NODE_VERSION'.split('.').map(Number);process.exit(a[0]>b[0]||a[0]===b[0]&&(a[1]>b[1]||a[1]===b[1]&&a[2]>=b[2])?0:1)"; then
  if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then source "${NVM_DIR:-$HOME/.nvm}/nvm.sh"; nvm install "$OLEANDER_COCOS_NODE_VERSION"; nvm use "$OLEANDER_COCOS_NODE_VERSION"; else echo "ERROR: Node >= $OLEANDER_COCOS_NODE_VERSION required; current=$current" >&2; exit 65; fi
fi
npm install -g node-gyp
if [[ ! -d "$DEST/engine/.git" ]]; then git clone https://github.com/cocos/cocos4.git "$DEST/engine"; fi
git -C "$DEST/engine" fetch --tags --force
git -C "$DEST/engine" checkout --detach "$OLEANDER_COCOS_ENGINE_SHA"
if [[ ! -d "$DEST/cli/.git" ]]; then git clone https://github.com/cocos/cocos-cli.git "$DEST/cli"; fi
git -C "$DEST/cli" fetch --all --tags --force
git -C "$DEST/cli" checkout --detach "$OLEANDER_COCOS_CLI_SHA"
pushd "$DEST/cli" >/dev/null
npm run init
npm install
npm run download-tools
npm run build
npm link
popd >/dev/null
install -m 0755 "$SCRIPT_DIR/bin/oleander-cocos" /usr/local/bin/oleander-cocos
cp "$SCRIPT_DIR/doctor.sh" "$DEST/doctor.sh"
chmod +x "$DEST/doctor.sh"
oleander-cocos doctor
