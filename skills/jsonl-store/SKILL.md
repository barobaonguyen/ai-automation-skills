---
name: jsonl-store
description: "Persist records between scheduled runs as append-only JSON Lines (one object per line) with streaming reads and optional key-based dedup, stdlib only. Use when the user wants to log run results to JSONL, append events to a file, dedup records by id across runs, or keep a simple durable history without a database."
version: "1.0.0"
---

# JSONL Store

Use this skill when a scheduled job needs to remember what it has already done - emitted alerts, processed ids, captured events - but a database is overkill. JSON Lines (one JSON object per line) is append-friendly, human-readable, greppable, and streams without loading the whole file. This helper adds atomic appends, streamed reads that survive a corrupt line, and `append_unique(record, key)` so the same id is never written twice across runs.

## When to invoke

- User says: "log results to a JSONL file", "append events to disk", "dedup by id across runs", "keep a simple history without a DB".
- A cron/scheduled script needs durable, between-run state in a flat file.

## When NOT to invoke

- You need queries, indexes, or concurrent writers - use SQLite (`sqlite-state`) or a real DB.
- Records are huge or binary - JSONL is for small structured rows.

## Concrete example

User input:

```text
After each run, append new alerts to alerts.jsonl but never the same alert id twice.
```

Output:

```python
# Copy assets/store.py into your project, then:
from store import JsonlStore

store = JsonlStore("data/alerts.jsonl")
for alert in new_alerts:
    if store.append_unique(alert, key="id"):
        send(alert)        # only fires for ids not seen in any prior run

print("history size:", store.count())
```

Reads stream line by line, so a year of history never loads fully into memory, and a half-written final line from a crash is skipped instead of breaking the next run.

## Pattern to apply

1. One JSON object per line; append with `ensure_ascii=False` so text stays readable.
2. Stream reads with a generator; skip blank/corrupt lines rather than raising.
3. Dedup with `seen_keys(key)` / `append_unique(record, key)` to make runs idempotent.
4. Pair with a scheduler so the file is the durable memory between invocations.

Reference: `assets/store.py`.

## Source

Distilled from the author's scheduled-bot state handling. v1.0.0.
See also: [[sqlite-state]], [[cron-dispatch]], [[pipeline-orchestrator]].

→ Build the full runnable bot with Trawlkit.
