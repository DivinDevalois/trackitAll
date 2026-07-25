#!/usr/bin/env bash
set -euo pipefail

# Backs up the TrackItAll Postgres database to a timestamped SQL file,
# on top of (not instead of) the Docker volume — a second copy in case
# the volume is ever deleted or corrupted. Keeps the last 30 backups.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$REPO_ROOT/backups"
KEEP_LAST=30

# shellcheck disable=SC1091
source "$REPO_ROOT/.env"

mkdir -p "$BACKUP_DIR"

TIMESTAMP="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_FILE="$BACKUP_DIR/trackitall_${TIMESTAMP}.sql"

cd "$REPO_ROOT"
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_FILE"

echo "Backup written to $BACKUP_FILE"

# Delete anything past the last $KEEP_LAST backups.
# (macOS ships BSD xargs, which has no -r; guard against empty input instead.)
OLD_BACKUPS="$(ls -1t "$BACKUP_DIR"/trackitall_*.sql 2>/dev/null | tail -n +$((KEEP_LAST + 1)))"
if [ -n "$OLD_BACKUPS" ]; then
  echo "$OLD_BACKUPS" | xargs rm --
fi
