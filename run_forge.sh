#!/bin/sh
set -e

PREFIX="${1:-docs: update activity}"

cd /app

# Ensure we're on the right branch
git fetch origin main
git checkout main
git pull origin main

git add -A

DATE=$(date -u +%Y-%m-%d)

if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "${PREFIX} ${DATE} $(date -u +%H:%M)"
  git push origin main
fi
