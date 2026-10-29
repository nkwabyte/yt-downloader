#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $(basename "$0") <youtube-url> [download-dir]"
    echo "  <youtube-url>   URL of the YouTube video or playlist"
    echo "  [download-dir]  Destination folder (default: ~/Downloads)"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
URL="$1"
OUT_DIR="${2:-$HOME/Downloads}"
shift $(( $# >= 2 ? 2 : 1 ))

exec uv run "$REPO_DIR/downloader.py" "$URL" "$OUT_DIR" "$@"

