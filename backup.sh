#!/usr/bin/env bash
# backup.sh : safe copy of the msk-dashboard database, kept locally and pushed off-box.
# Uses SQLite's backup API (safe while the server runs). Keeps the 30 newest
# local copies, then sends the newest to the Mac mini like health/backup.sh.
# Run by hand any time:   bash backup.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB="${MSK_DB:-$HOME/.local/share/msk-dashboard/dashboard.db}"
OUT_DIR="${BACKUP_DIR:-$HOME/.local/share/msk-dashboard/backups}"
KEEP=30

mkdir -p "$OUT_DIR"
STAMP="$(date +%Y-%m-%d_%H%M%S)"
TARGET="$OUT_DIR/mskdash_$STAMP.db"

python3 - "$DB" "$TARGET" <<'PY'
import sqlite3, sys
source = sqlite3.connect(sys.argv[1])
target = sqlite3.connect(sys.argv[2])
with target:
    source.backup(target)
target.close()
source.close()
PY

echo "Backup written: $TARGET"

ls -1t "$OUT_DIR"/mskdash_*.db 2>/dev/null | tail -n +"$((KEEP + 1))" | while read -r old; do
  rm -f -- "$old"
done

# Push the newest copy to the Mac mini over Tailscale with the same restricted
# key Health uses (forced command: can only write into that one remote directory).
# -O forces legacy SCP; see health/backup.sh for why.
REMOTE_HOST="markkelly@100.80.137.8"
REMOTE_DIR="/Volumes/4TBSSD/backups/"
REMOTE_KEY="$HOME/.ssh/health_backup"
if scp -O -o BatchMode=yes -o ConnectTimeout=10 -i "$REMOTE_KEY" "$TARGET" "$REMOTE_HOST:$REMOTE_DIR"; then
  echo "Off-box copy sent: $REMOTE_HOST:$REMOTE_DIR$(basename "$TARGET")"
else
  echo "WARNING: off-box copy failed; $TARGET stays local only" >&2
  exit 1
fi
