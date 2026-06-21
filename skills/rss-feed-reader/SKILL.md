---
name: rss-feed-reader
description: "Parse an RSS 2.0 or Atom feed into normalized item dicts (title, link, id, published, summary) with the standard library only - no feedparser. Use when the user asks to read an RSS/Atom feed, poll a blog/news feed, extract feed entries, or watch a site that publishes a feed."
version: "1.0.0"
---

# RSS / Atom Feed Reader

Use this skill when a script needs to read a feed and you want one normalized shape across both RSS 2.0 and Atom, with no third-party dependency. It does a single `ElementTree` pass and pulls `title`, `link`, `id`, `published`, and `summary` from either format, so downstream code (dedup, digest, alert) never has to branch on feed type.

## When to invoke

- User says: "read this RSS feed", "poll a blog feed", "get the latest entries from an Atom feed", "watch a site for new posts".
- Code already fetched feed bytes and needs structured entries.

## When NOT to invoke

- The source has a real JSON API - call that instead of scraping a feed.
- You need full feedparser quirks handling (every malformed dialect) - install `feedparser`.

## Concrete example

User input:

```text
Read https://example.com/feed.xml and print each post title and link.
```

Output:

```python
# Copy assets/feed.py into your project, then:
from urllib.request import urlopen
from feed import parse_feed

with urlopen("https://example.com/feed.xml", timeout=20) as r:
    for item in parse_feed(r.read()):
        print(item["title"], "->", item["link"])
```

Every item is a dict with the same keys whether the feed is RSS or Atom, so dedup by `id` and sort by `published` work without special-casing.

## Pattern to apply

1. Parse once with `xml.etree.ElementTree`; iterate `item` (RSS) and `{atom}entry` (Atom).
2. Normalize to a stable key set so the rest of the pipeline is feed-format agnostic.
3. Fall back from `guid`/atom `id` to the link so every item has a stable identity for dedup.
4. Keep network out of the parser: pass in bytes/text so it stays pure and testable.

Reference: `assets/feed.py`.

## Source

Distilled from the author's news-aggregation projects. v1.0.0.
See also: [[gmail-imap-digest]], [[sqlite-state]], [[pipeline-orchestrator]].

→ Build the full runnable bot with Trawlkit.
