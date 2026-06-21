"""Parse RSS 2.0 and Atom feeds into normalized item dicts. Stdlib only.

No feedparser dependency: this reads the common fields (title, link, id,
published, summary) from both RSS and Atom with a single ElementTree pass.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

_ATOM = "{http://www.w3.org/2005/Atom}"


def _text(node: ET.Element | None) -> str:
    return (node.text or "").strip() if node is not None else ""


def _atom_link(entry: ET.Element) -> str:
    # Prefer rel="alternate"; fall back to the first link with an href.
    fallback = ""
    for link in entry.findall(f"{_ATOM}link"):
        href = link.get("href", "")
        if link.get("rel", "alternate") == "alternate" and href:
            return href
        fallback = fallback or href
    return fallback


def parse_feed(content: str | bytes) -> list[dict[str, Any]]:
    """Return a list of ``{title, link, id, published, summary}`` item dicts."""
    root = ET.fromstring(content)
    items: list[dict[str, Any]] = []

    # RSS 2.0: <rss><channel><item>...
    for item in root.iter("item"):
        items.append(
            {
                "title": _text(item.find("title")),
                "link": _text(item.find("link")),
                "id": _text(item.find("guid")) or _text(item.find("link")),
                "published": _text(item.find("pubDate")),
                "summary": _text(item.find("description")),
            }
        )

    # Atom: <feed><entry>...
    for entry in root.iter(f"{_ATOM}entry"):
        items.append(
            {
                "title": _text(entry.find(f"{_ATOM}title")),
                "link": _atom_link(entry),
                "id": _text(entry.find(f"{_ATOM}id")),
                "published": _text(entry.find(f"{_ATOM}updated"))
                or _text(entry.find(f"{_ATOM}published")),
                "summary": _text(entry.find(f"{_ATOM}summary"))
                or _text(entry.find(f"{_ATOM}content")),
            }
        )
    return items


if __name__ == "__main__":  # pragma: no cover
    import sys
    from urllib.request import urlopen

    with urlopen(sys.argv[1], timeout=20) as response:  # noqa: S310
        for entry in parse_feed(response.read()):
            print(entry["title"], "->", entry["link"])
