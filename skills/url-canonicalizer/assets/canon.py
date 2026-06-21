"""Canonicalize URLs so the same page dedupes to one key. Stdlib only.

Lowercases scheme/host, drops the default port and a trailing-slash-only path,
removes the fragment, strips common tracking params (utm_*, fbclid, gclid, ref,
...), and sorts the remaining query so order never changes the key.
"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_TRACKING_PREFIXES = ("utm_",)
_TRACKING_EXACT = {
    "fbclid", "gclid", "gclsrc", "dclid", "msclkid", "mc_cid", "mc_eid",
    "ref", "ref_src", "igshid", "yclid", "_ga", "spm",
}
_DEFAULT_PORTS = {"http": "80", "https": "443"}


def _is_tracking(key: str) -> bool:
    low = key.lower()
    return low in _TRACKING_EXACT or any(low.startswith(p) for p in _TRACKING_PREFIXES)


def canonicalize(url: str, *, keep_query: bool = True) -> str:
    """Return a canonical form of ``url`` suitable for dedup keys."""
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()
    host = parts.hostname or ""

    netloc = host
    if parts.port and str(parts.port) != _DEFAULT_PORTS.get(scheme):
        netloc = f"{host}:{parts.port}"

    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    query = ""
    if keep_query and parts.query:
        kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not _is_tracking(k)]
        kept.sort()
        query = urlencode(kept)

    return urlunsplit((scheme, netloc, path, query, ""))  # fragment always dropped


def same_page(a: str, b: str) -> bool:
    """True when two URLs canonicalize to the same key."""
    return canonicalize(a) == canonicalize(b)


if __name__ == "__main__":  # pragma: no cover
    import sys

    for raw in sys.argv[1:]:
        print(canonicalize(raw))
