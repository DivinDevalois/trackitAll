#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "Starting Postgres..."
docker compose up -d
until docker compose exec -T db pg_isready -U trackitall -d trackitall > /dev/null 2>&1; do
  sleep 1
done
echo "Postgres ready."

echo "Starting API on :8000..."
(cd "$REPO_ROOT/backend" && uv run uvicorn app.main:app --port 8000 > "$REPO_ROOT/api.log" 2>&1 &)

echo "Starting Streamlit on :8501..."
(cd "$REPO_ROOT/frontend" && uv run streamlit run app.py --server.port 8501 --server.headless true > "$REPO_ROOT/streamlit.log" 2>&1 &)

sleep 3
echo ""
echo "TrackItAll is running:"
echo "  App:  http://127.0.0.1:8501"
echo "  API:  http://127.0.0.1:8000/docs"
echo ""
echo "To stop: ./stop.sh"
