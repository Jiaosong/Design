#!/usr/bin/env bash
set -euo pipefail
SOURCE="${1:-$(pwd)/05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source}"
DEST="${2:-$(pwd)/05-cases/c04-qingjiang-stone-book/game-ui/cocos4-project}"
if ! command -v oleander-cocos >/dev/null 2>&1; then echo "ERROR: oleander-cocos gateway missing" >&2; exit 69; fi
if [[ -e "$DEST" && -n "$(ls -A "$DEST" 2>/dev/null || true)" ]]; then echo "ERROR: destination is not empty: $DEST" >&2; exit 73; fi
mkdir -p "$DEST"
oleander-cocos create "$DEST" 2d
mkdir -p "$DEST/assets"
cp -R "$SOURCE/assets/." "$DEST/assets/"
oleander-cocos import "$DEST"
oleander-cocos info "$DEST"
echo "C04 materialized as a real COCOS CLI project at: $DEST"
