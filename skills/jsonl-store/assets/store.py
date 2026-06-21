"""A durable append-only JSON Lines store for between-run records. Stdlib only.

Each record is one JSON object per line. Appends are atomic per write, reads are
streamed so a large log never loads fully into memory, and optional key-dedup
skips records whose key has already been written.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class JsonlStore:
    """Append-only JSON Lines file with streaming reads and optional key dedup."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, record: dict[str, Any]) -> None:
        """Append one record as a JSON line, creating the file if needed."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def iter_records(self) -> Iterator[dict[str, Any]]:
        """Yield each record. Blank or corrupt lines are skipped, not fatal."""
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue

    def read_all(self) -> list[dict[str, Any]]:
        return list(self.iter_records())

    def seen_keys(self, key: str) -> set[str]:
        """Set of values already present for ``key`` (for dedup)."""
        return {str(r[key]) for r in self.iter_records() if key in r}

    def append_unique(self, record: dict[str, Any], key: str) -> bool:
        """Append only if ``record[key]`` is new. Returns True when written."""
        if str(record.get(key)) in self.seen_keys(key):
            return False
        self.append(record)
        return True

    def count(self) -> int:
        return sum(1 for _ in self.iter_records())
