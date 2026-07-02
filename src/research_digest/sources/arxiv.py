"""Fetch recent papers from the arXiv API.

The arXiv API returns an Atom feed which we parse with feedparser. Docs:
https://info.arxiv.org/help/api/user-manual.html
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from ..models import Paper

ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "research-digest/0.1 (+https://github.com/OpenScience-Collective)"


def _parse_dt(value: str) -> datetime:
    # feedparser gives struct_time; but we parse the raw string for safety.
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except (ValueError, TypeError):
        return datetime.now(timezone.utc)


def _entry_to_paper(entry) -> Paper:
    arxiv_id = entry.get("id", "").rsplit("/abs/", 1)[-1]
    pdf_url = ""
    for link in entry.get("links", []):
        if link.get("type") == "application/pdf":
            pdf_url = link.get("href", "")
    if not pdf_url and arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

    categories = [t.get("term") for t in entry.get("tags", []) if t.get("term")]
    authors = [a.get("name") for a in entry.get("authors", []) if a.get("name")]

    return Paper(
        source="arxiv",
        paper_id=arxiv_id,
        title=" ".join(entry.get("title", "").split()),
        abstract=" ".join(entry.get("summary", "").split()),
        authors=authors,
        categories=categories,
        published=_parse_dt(entry.get("published", "")),
        updated=_parse_dt(entry.get("updated", "")),
        abstract_url=entry.get("id", ""),
        pdf_url=pdf_url,
    )


def fetch_recent(
    categories: list[str],
    lookback_days: int,
    max_candidates: int = 120,
    *,
    session: requests.Session | None = None,
    now: datetime | None = None,
) -> list[Paper]:
    """Return papers submitted within ``lookback_days`` for the given categories."""
    session = session or requests.Session()
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=lookback_days)

    query = " OR ".join(f"cat:{c}" for c in categories)
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": max_candidates,
    }
    resp = session.get(
        ARXIV_API, params=params, headers={"User-Agent": USER_AGENT}, timeout=30
    )
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)

    papers: list[Paper] = []
    for entry in feed.entries:
        paper = _entry_to_paper(entry)
        if paper.published >= cutoff:
            papers.append(paper)
    return papers
