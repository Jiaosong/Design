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

# Retry transient registry/network failures without weakening immutable SHA verification.
export npm_config_fetch_retries="${npm_config_fetch_retries:-5}"
export npm_config_fetch_retry_factor="${npm_config_fetch_retry_factor:-2}"
export npm_config_fetch_retry_mintimeout="${npm_config_fetch_retry_mintimeout:-1000}"
export npm_config_fetch_retry_maxtimeout="${npm_config_fetch_retry_maxtimeout:-20000}"

retry_cmd() {
  local attempt=1
  local max_attempts="${OLEANDER_COCOS_NETWORK_ATTEMPTS:-3}"
  local delay=3
  local status=0
  while true; do
    if "$@"; then
      return 0
    else
      status=$?
    fi
    if (( attempt >= max_attempts )); then
      echo "ERROR: command failed after $attempt attempts (exit=$status): $*" >&2
      return "$status"
    fi
    echo "WARN: transient command failure (attempt $attempt/$max_attempts, exit=$status); retrying: $*" >&2
    sleep "$delay"
    attempt=$((attempt + 1))
    delay=$((delay * 2))
  done
}

checkout_pinned_repo() {
  local repo_url="$1"
  local target="$2"
  local expected_sha="$3"
  local label="$4"

  if [[ ! -d "$target/.git" ]]; then
    rm -rf "$target"
    mkdir -p "$target"
    git -C "$target" init
    git -C "$target" remote add origin "$repo_url"
  else
    git -C "$target" remote set-url origin "$repo_url"
  fi

  retry_cmd git -C "$target" fetch --no-tags --depth=1 origin "$expected_sha"
  git -C "$target" checkout --detach FETCH_HEAD
  local actual_sha
  actual_sha="$(git -C "$target" rev-parse HEAD)"
  if [[ "$actual_sha" != "$expected_sha" ]]; then
    echo "ERROR: $label SHA mismatch: expected=$expected_sha actual=$actual_sha" >&2
    exit 66
  fi
  echo "$label pinned checkout: $actual_sha"
}

retry_cmd npm install -g node-gyp

if [[ ! -d "$DEST/cli/.git" ]]; then
  retry_cmd git clone https://github.com/cocos/cocos-cli.git "$DEST/cli"
fi
retry_cmd git -C "$DEST/cli" fetch origin "$OLEANDER_COCOS_CLI_SHA"
git -C "$DEST/cli" checkout --detach "$OLEANDER_COCOS_CLI_SHA"

actual_cli="$(git -C "$DEST/cli" rev-parse HEAD)"
if [[ "$actual_cli" != "$OLEANDER_COCOS_CLI_SHA" ]]; then
  echo "ERROR: CLI SHA mismatch: expected=$OLEANDER_COCOS_CLI_SHA actual=$actual_cli" >&2
  exit 66
fi

# Do not use `npm run init` here: pinned cocos-cli resolves repo.json through mutable tags.
# Materialize engine/external from immutable OLEANDER SHAs, then run the same install/build phases.
ENGINE_DIR="$DEST/cli/packages/engine"
EXTERNAL_DIR="$ENGINE_DIR/native/external"
checkout_pinned_repo https://github.com/cocos/cocos4.git "$ENGINE_DIR" "$OLEANDER_COCOS_ENGINE_SHA" "Engine"
checkout_pinned_repo https://github.com/cocos/cocos-engine-external.git "$EXTERNAL_DIR" "$OLEANDER_COCOS_EXTERNAL_SHA" "Engine external"

pushd "$DEST/cli" >/dev/null
retry_cmd npm run install:engine
retry_cmd npm install
npm run download-tools
npm run build
popd >/dev/null

actual_engine="$(git -C "$ENGINE_DIR" rev-parse HEAD)"
if [[ "$actual_engine" != "$OLEANDER_COCOS_ENGINE_SHA" ]]; then
  echo "ERROR: Engine SHA mismatch: expected=$OLEANDER_COCOS_ENGINE_SHA actual=$actual_engine" >&2
  exit 68
fi
actual_external="$(git -C "$EXTERNAL_DIR" rev-parse HEAD)"
if [[ "$actual_external" != "$OLEANDER_COCOS_EXTERNAL_SHA" ]]; then
  echo "ERROR: Engine external SHA mismatch: expected=$OLEANDER_COCOS_EXTERNAL_SHA actual=$actual_external" >&2
  exit 71
fi
if [[ ! -f "$DEST/cli/dist/cli.js" ]]; then
  echo "ERROR: COCOS CLI build did not produce dist/cli.js" >&2
  exit 69
fi

install -m 0755 "$SCRIPT_DIR/bin/oleander-cocos" "$BIN_DIR/oleander-cocos"
"$BIN_DIR/oleander-cocos" doctor

echo "OLEANDER COCOS 4 shared toolchain installed: $DEST"
echo "Gateway: $BIN_DIR/oleander-cocos"
