"""
dep_audit.py — checks latest versions of a curated package list and logs findings.
Writes to deps/audit-YYYY-MM-DD.md
"""
import urllib.request
import json
import os
from datetime import datetime, timezone

PACKAGES = {
    "npm": [
        "react", "typescript", "vite", "tailwindcss", "axios",
        "zustand", "tanstack/react-query", "zod", "eslint", "prettier",
        "next", "fastapi", "uvicorn", "pydantic", "httpx",
    ],
    "pypi": [
        "django", "fastapi", "pydantic", "sqlalchemy", "alembic",
        "celery", "redis", "httpx", "pytest", "black",
        "ruff", "mypy", "boto3", "pillow", "numpy",
    ],
}

def get_npm_version(pkg):
    try:
        url = f"https://registry.npmjs.org/{pkg}/latest"
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read())["version"]
    except Exception:
        return "unavailable"

def get_pypi_version(pkg):
    try:
        url = f"https://pypi.org/pypi/{pkg}/json"
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read())["info"]["version"]
    except Exception:
        return "unavailable"

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")

    lines = [
        f"# Dependency Audit — {date_str} {time_str}",
        "",
        "## npm packages",
        "",
        "| Package | Latest |",
        "|---------|--------|",
    ]
    for pkg in PACKAGES["npm"]:
        v = get_npm_version(pkg)
        lines.append(f"| {pkg} | {v} |")

    lines += ["", "## PyPI packages", "", "| Package | Latest |", "|---------|--------|"]
    for pkg in PACKAGES["pypi"]:
        v = get_pypi_version(pkg)
        lines.append(f"| {pkg} | {v} |")

    lines += ["", f"*Generated at {time_str}*", ""]

    os.makedirs("deps", exist_ok=True)
    out = f"deps/audit-{date_str}.md"
    with open(out, "w") as f:
        f.write("\n".join(lines))

    print(f"dep-audit: wrote {out}")
    return out

if __name__ == "__main__":
    main()
