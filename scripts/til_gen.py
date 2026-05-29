"""
til_gen.py — writes a Today-I-Learned entry from a rotating topic list.
Writes to til/YYYY-MM-DD-HH.md
"""
import os
import hashlib
from datetime import datetime, timezone

TOPICS = [
    ("Python GIL", "The Global Interpreter Lock prevents true multi-threading in CPython. Use `multiprocessing` or async I/O instead for CPU-bound or I/O-bound work respectively."),
    ("TCP 3-way handshake", "SYN → SYN-ACK → ACK. The client sends SYN, server replies SYN-ACK, client confirms with ACK. After this the connection is established and data can flow."),
    ("CAP Theorem", "A distributed system can guarantee at most 2 of: Consistency, Availability, Partition tolerance. Most real systems choose AP or CP depending on the use case."),
    ("B-Tree indexes", "Database B-Tree indexes keep data sorted and allow searches, insertions, and deletions in O(log n). They're the default index type in Postgres and MySQL."),
    ("CSS Stacking Context", "A new stacking context is created by position+z-index, opacity < 1, transform, filter, etc. z-index only competes within the same stacking context."),
    ("HTTP/2 multiplexing", "HTTP/2 sends multiple requests over a single TCP connection using streams, eliminating head-of-line blocking at the HTTP layer (though TCP HOL still exists)."),
    ("Bloom filters", "A space-efficient probabilistic data structure that tests set membership. False positives are possible; false negatives are not. Used in databases and caches."),
    ("React reconciliation", "React diffs the virtual DOM tree using a heuristic O(n) algorithm. Keys help it identify moved list items and avoid unnecessary re-renders."),
    ("JWT structure", "A JWT is base64url(header).base64url(payload).signature. The signature is verified server-side; the payload is readable by anyone — don't put secrets in it."),
    ("ACID vs BASE", "ACID (relational DBs): Atomicity, Consistency, Isolation, Durability. BASE (NoSQL): Basically Available, Soft state, Eventual consistency."),
    ("Docker layer caching", "Each Dockerfile instruction creates a layer. Layers are cached; a change invalidates that layer and all subsequent ones. Put rarely-changing steps first."),
    ("async/await under the hood", "async/await in Python is syntactic sugar over coroutines and an event loop (asyncio). `await` suspends the coroutine until the awaitable completes."),
    ("WebSockets", "After an HTTP upgrade handshake, WebSockets provide a full-duplex channel over a single TCP connection. Unlike HTTP, the server can push without a request."),
    ("Consistent hashing", "Distributes keys across nodes so that only K/n keys need remapping when a node is added/removed (K=keys, n=nodes). Used in distributed caches like Redis Cluster."),
    ("SQL EXPLAIN", "EXPLAIN (or EXPLAIN ANALYZE) shows the query plan the DB optimizer chose. Look for Seq Scan on large tables — that's a missing index."),
    ("Git reflog", "`git reflog` records every HEAD movement. You can recover 'lost' commits after a reset or rebase by finding the hash and checking it out."),
    ("CORS preflight", "Browsers send an OPTIONS preflight for cross-origin requests that use non-simple methods or headers. The server must respond with the right Access-Control headers."),
    ("Indexes and writes", "Every index speeds up reads but slows down writes (INSERT/UPDATE/DELETE must update all indexes). Don't over-index write-heavy tables."),
    ("Tail call optimization", "In languages that support TCO (e.g. Scheme, some JS engines), a recursive call in tail position doesn't add a new stack frame, avoiding stack overflow."),
    ("Redis data types", "Redis supports strings, lists, sets, sorted sets, hashes, streams, and more. Choosing the right type (e.g. sorted set for leaderboards) gives O(log n) ops for free."),
    ("Kubernetes liveness vs readiness", "Liveness probes restart a stuck container. Readiness probes remove it from the Service endpoints until it's ready. Use both for robust deployments."),
    ("Memoization", "Cache the result of a function for a given input so repeated calls skip recomputation. Python's `functools.lru_cache` does this with one decorator."),
    ("Content Security Policy", "CSP headers tell browsers which sources are allowed for scripts, styles, images, etc. A strict CSP is one of the best defenses against XSS."),
    ("Event sourcing", "Store state as an immutable log of events rather than current values. Replay the log to rebuild state at any point in time. Used in audit systems and CQRS."),
    ("TypeScript discriminated unions", "A union type where each member has a literal field (e.g. `type`) lets TypeScript narrow the type inside if/switch blocks automatically."),
    ("SQL window functions", "Window functions (ROW_NUMBER, RANK, LAG, SUM OVER) compute values across a set of rows related to the current row without collapsing them like GROUP BY."),
    ("Python dataclasses", "`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__`. Add `frozen=True` for immutability or `slots=True` (3.10+) for memory efficiency."),
    ("Zero-copy I/O", "sendfile() and splice() let the kernel transfer data between file descriptors without copying to user space. Used in high-performance servers like Nginx."),
    ("Merkle trees", "A tree where each node is a hash of its children. Used in Git (content-addressable objects), blockchains, and distributed file systems to verify integrity efficiently."),
    ("Rate limiting algorithms", "Token bucket allows bursts; leaky bucket smooths output. Sliding window log is accurate; fixed window is simple. Redis + Lua scripts implement most of these."),
]

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    time_str = now.strftime("%H:%M UTC")

    # rotate deterministically by day+hour
    idx = int(hashlib.md5(f"{date_str}-{hour_str}".encode()).hexdigest(), 16) % len(TOPICS)
    title, body = TOPICS[idx]

    content = f"# TIL: {title}\n\n_{date_str} {time_str}_\n\n{body}\n"

    os.makedirs("til", exist_ok=True)
    out = f"til/{date_str}-{hour_str}.md"
    with open(out, "w") as f:
        f.write(content)

    print(f"til: wrote {out} — {title}")
    return out

if __name__ == "__main__":
    main()
