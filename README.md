# Daily Activity Forge

An automated dev activity system that runs every 3 hours, 24/7.

Each run does one of several **real, meaningful tasks**:

| Task | What it does |
|------|-------------|
| `dep-audit` | Scans popular npm/pip packages for version updates, logs findings |
| `til` | Adds a Today-I-Learned entry from a rotating CS/dev topic list |
| `algo` | Adds a new algorithm snippet (Python) to a growing collection |
| `devlog` | Writes a timestamped dev journal entry |
| `weekly-pr` | Opens a PR summarizing the week's activity (Sundays) |

## Stats

See [activity.log](./activity.log) for the full run history.
