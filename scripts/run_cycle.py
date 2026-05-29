"""
run_cycle.py — dispatcher that picks which task(s) to run each cycle.

Schedule logic (UTC hour):
  00, 03, 06, 09 → TIL entry
  12, 15         → Algorithm snippet
  18, 21         → Dev log
  Every run      → Dep audit (once per day, skips if today's file exists)

Returns the list of files written (used by the GitHub Action for the commit message).
"""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))

import dep_audit
import til_gen
import algo_gen
import devlog_gen

def main():
    now = datetime.now(timezone.utc)
    hour = now.hour
    date_str = now.strftime("%Y-%m-%d")

    written = []

    # dep audit — once per day
    audit_path = f"deps/audit-{date_str}.md"
    if not os.path.exists(audit_path):
        written.append(dep_audit.main())

    # rotate content tasks by hour bucket
    if hour in (0, 3, 6, 9):
        written.append(til_gen.main())
    elif hour in (12, 15):
        written.append(algo_gen.main())
    elif hour in (18, 21):
        written.append(devlog_gen.main())
    else:
        # off-schedule hours: just write a TIL
        written.append(til_gen.main())

    # append to activity log
    with open("activity.log", "a") as f:
        for path in written:
            f.write(f"{now.isoformat()} {path}\n")

    print(f"cycle complete: {written}")
    return written

if __name__ == "__main__":
    main()
