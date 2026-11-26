#!/bin/sh
# Retention: delete dated til/devlog/algos entries older than RETENTION_DAYS.
# File names start with YYYY-MM-DD; entries on or after the cutoff are kept.
set -e

cd /app

RETENTION_DAYS="${RETENTION_DAYS:-400}"
CUTOFF=$(date -u -d "$RETENTION_DAYS days ago" +%Y-%m-%d)

removed=0
for dir in til devlog algos; do
    [ -d "$dir" ] || continue
    stale=$(find "$dir" -maxdepth 1 -type f -printf '%f\n' 2>/dev/null \
        | awk -v c="$CUTOFF" '/^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ { if (substr($0, 1, 10) < c) print }')
    [ -n "$stale" ] || continue
    for name in $stale; do
        rm -f "$dir/$name"
        removed=$((removed + 1))
    done
done

echo "prune_old: removed $removed file(s) older than $CUTOFF (${RETENTION_DAYS}d retention)"
