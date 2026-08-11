#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "==> Building frontend"
cd frontend
npm install
npm run build
cd "$ROOT_DIR"

echo "==> Starting backend"
PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"   python "$ROOT_DIR/src/research_paper_ai/api/app.py"
