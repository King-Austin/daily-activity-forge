"""
devlog_gen.py — writes a timestamped dev journal entry.
Writes to devlog/YYYY-MM-DD-HH.md
"""
import os
import hashlib
from datetime import datetime, timezone

ENTRIES = [
    ("Refactoring session", "Spent time reviewing module boundaries and reducing coupling between components. Identified two abstractions that can be merged without losing clarity."),
    ("Performance profiling", "Ran a profile on the hot path. Found that most time is spent in I/O, not compute. Switched to async calls and saw a measurable latency drop."),
    ("Code review notes", "Reviewed open PRs. Left feedback on error handling patterns — prefer explicit error types over generic exceptions. Also flagged a missing index on a FK column."),
    ("Dependency updates", "Bumped several packages to latest stable. Checked changelogs for breaking changes before merging. One package had a subtle API rename worth noting."),
    ("Database query audit", "Examined slow query log. Two queries missing indexes; one with an unnecessary subquery that can be rewritten as a JOIN. Filed tickets for both."),
    ("Documentation pass", "Updated inline docs for the auth module. Removed outdated comments, clarified parameter contracts, added examples for the most-called functions."),
    ("Security review", "Reviewed input validation across API endpoints. All user-supplied strings are properly escaped. Rate limiting is in place on auth routes. CORS policy is restrictive."),
    ("Test coverage review", "Generated coverage report. Core business logic is at 87%. Edge cases around timezone handling are undertested — added two new test cases."),
    ("CI/CD pipeline review", "Checked pipeline run times. Parallelised the lint and test stages; cut total time by about 30%. Also added a cache step for dependency installs."),
    ("Architecture notes", "Sketched out service boundaries for the next feature. Leaning toward an event-driven pattern here rather than direct RPC to avoid tight coupling."),
    ("Debugging session", "Tracked down a subtle race condition in the job queue. Root cause: shared mutable state across workers. Fixed by passing immutable snapshots instead."),
    ("API design review", "Reviewed the new endpoint contract. Settled on returning 202 Accepted for async jobs with a polling URL in the response body, following REST conventions."),
    ("Monitoring and alerts", "Set up structured log queries for error rates and p99 latency. Configured alerts for anything above baseline. Added a dashboard panel for queue depth."),
    ("Onboarding notes", "Improved the local dev setup guide. Reduced steps from 12 to 7 by scripting the environment bootstrap. First-run time is now under 5 minutes."),
    ("Feature flag review", "Audited active feature flags. Cleaned up three that are fully rolled out. Simplified the branching logic in two components as a result."),
    ("Load testing", "Ran a load test against the staging environment. System handles expected peak load with headroom. Identified one endpoint that degrades under sustained concurrency — queued for optimization."),
    ("Incident retrospective", "Wrote up a post-mortem for last week's incident. Root cause: a missing retry on an external API call. Added exponential backoff with jitter as the fix."),
    ("RFC drafting", "Drafted an RFC for the new caching strategy. Proposing a write-through cache at the service layer with a 5-minute TTL. Shared for async review."),
    ("Pair programming notes", "Paired on the new payment flow. Caught an edge case where a failed charge could leave an order in a pending state indefinitely. Added a reconciliation job."),
    ("Release prep", "Tagged the release candidate. Ran through the deployment checklist: migrations, rollback plan, feature flag states, on-call rotation confirmed."),
]

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    time_str = now.strftime("%H:%M UTC")

    idx = int(hashlib.md5(f"{date_str}-{hour_str}-devlog".encode()).hexdigest(), 16) % len(ENTRIES)
    title, body = ENTRIES[idx]

    content = f"# {title}\n\n_{date_str} {time_str}_\n\n{body}\n"

    os.makedirs("devlog", exist_ok=True)
    out = f"devlog/{date_str}-{hour_str}.md"
    with open(out, "w") as f:
        f.write(content)

    print(f"devlog: wrote {out} — {title}")
    return out

if __name__ == "__main__":
    main()
