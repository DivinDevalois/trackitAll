#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

pkill -f "uvicorn app.main:app" 2>/dev/null && echo "API stopped." || echo "API was not running."
pkill -f "streamlit run app.py" 2>/dev/null && echo "Streamlit stopped." || echo "Streamlit was not running."

docker compose stop
echo "Postgres stopped (data preserved)."
