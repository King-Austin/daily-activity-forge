#!/bin/sh
set -e

cd /app

git fetch origin main
git checkout main
git pull origin main

WEEK=$(date -u +%Y-W%V)
BRANCH="weekly-summary-${WEEK}"

# Checkout new branch
git checkout -b $BRANCH

SINCE=$(date -u -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d 2>/dev/null || echo "")
# Simple count if SINCE fails
if [ -z "$SINCE" ]; then
    TIL_COUNT=$(ls til/ 2>/dev/null | wc -l)
    ALGO_COUNT=$(ls algos/ 2>/dev/null | wc -l)
    LOG_COUNT=$(ls devlog/ 2>/dev/null | wc -l)
else
    TIL_COUNT=$(ls til/ 2>/dev/null | grep -c "^${SINCE:0:7}" || echo 0)
    ALGO_COUNT=$(ls algos/ 2>/dev/null | grep -c "^${SINCE:0:7}" || echo 0)
    LOG_COUNT=$(ls devlog/ 2>/dev/null | grep -c "^${SINCE:0:7}" || echo 0)
fi

mkdir -p summaries

cat > "summaries/week-${WEEK}.md" << EOF
# Weekly Summary — ${WEEK}

_Generated $(date -u +"%Y-%m-%d %H:%M UTC")_

## Activity This Week

| Type | Count |
|------|-------|
| TIL entries | ${TIL_COUNT} |
| Algorithm snippets | ${ALGO_COUNT} |
| Dev log entries | ${LOG_COUNT} |

## Recent TIL Entries

$(ls til/ 2>/dev/null | tail -5 | sed 's/^/- /')

## Recent Algorithms

$(ls algos/ 2>/dev/null | tail -5 | sed 's/^/- /')
EOF

git add -A

if git diff --cached --quiet; then
  echo "No changes for weekly summary."
else
  git commit -m "docs: weekly summary ${WEEK}"
  git push origin $BRANCH

  export GH_TOKEN=$GITHUB_TOKEN
  gh pr create \
    --title "Weekly summary ${WEEK}" \
    --body "Auto-generated weekly activity summary. Covers TIL entries, algorithm snippets, and dev log updates from the past 7 days." \
    --base main \
    --head "$BRANCH" \
    --label "automated"

  # Merge the PR
  PR=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number')
  if [ -n "$PR" ]; then
    gh pr merge $PR --merge --delete-branch
  fi
fi

git checkout main
