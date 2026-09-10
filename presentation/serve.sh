#!/usr/bin/env bash
#
# Build the Marp deck (with Shiki highlighting + line numbers) and serve it
# over HTTP with Python's built-in server.
#
# Usage:
#   ./serve.sh          # build once, serve on port 8000
#   ./serve.sh 8080     # build once, serve on a custom port
#
set -euo pipefail

# Directory this script lives in (the presentation/ folder), so it works
# regardless of the current working directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${1:-8000}"

echo "==> Building presentation.html with the Shiki engine..."
( cd tooling && npm run build )

echo "==> Serving http://localhost:${PORT}/presentation.html"
echo "    Press Ctrl+C to stop."
python3 -m http.server "$PORT"
