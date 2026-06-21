---
name: url-canonicalizer
description: "Normalize URLs to a canonical form (lowercase host, drop default port and trailing slash, remove fragment, strip utm_/fbclid/gclid tracking params, sort the query) so the same page dedupes to one key - stdlib only. Use when the user wants to dedup links across sources, normalize scraped URLs, or build a stable seen-set key from a URL."
version: "1.0.0"
---

# URL Canonicalizer

Use this skill when the same page arrives as several different URL strings - one with `?utm_source=...`, one with a trailing slash, one with a `#section` fragment, one with the query params in a different order - and you need them all to dedupe to a single key. It lowercases the scheme/host, drops default ports and a trailing-slash-only path, removes the fragment, strips common tracking params, and sorts the rest of the query, so `seen.add(canonicalize(url))` actually catches duplicates.

## When to invoke

- User says: "dedup these links", "normalize scraped URLs", "stop re-posting the same article", "build a stable key from a URL".
- Items come from multiple feeds/sources and the same story has slightly different URLs.

## When NOT to invoke

- You must preserve the exact original URL (it is a signed/one-time link) - keep it as-is.
- Two paths are genuinely different pages that happen to share a query - don't over-normalize.

## Concrete example

User input:

```text
These two links are the same article; make my seen-set treat them as one.
```

Output:

```python
# Copy assets/canon.py into your project, then:
from canon import canonicalize, same_page

a = "https://Example.com/Post/?utm_source=tw&ref=home#top"
b = "https://example.com/Post"
canonicalize(a)      # "https://example.com/Post"
same_page(a, b)      # True

seen = set()
if (key := canonicalize(url)) not in seen:
    seen.add(key)
    process(url)
```

Tracking params (`utm_*`, `fbclid`, `gclid`, `ref`, ...) and the fragment are dropped, the query is sorted, and the host is lowercased, so cosmetic differences collapse to one key.

## Pattern to apply

1. Split with `urllib.parse.urlsplit`; lowercase scheme and host (but not the path - paths can be case-sensitive).
2. Drop the default port, a trailing-slash-only path, and the fragment.
3. Remove tracking params and sort the remainder so query order is irrelevant.
4. Use the canonical string as the dedup/seen-set key, not the raw URL.

Reference: `assets/canon.py`.

## Source

Distilled from the author's multi-source dedup pipelines. v1.0.0.
See also: [[jsonl-store]], [[rss-feed-reader]], [[sqlite-state]].

→ Build the full runnable bot with Trawlkit.
