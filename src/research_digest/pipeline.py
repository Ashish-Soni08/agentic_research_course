"""Orchestrate the full nightly run: fetch -> rank -> find code -> summarize -> write."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

import requests

from . import code_finder, digest, ranking, summarizer
from .config import Config
from .models import Paper
from .sources import arxiv


def run(
    config: Config,
    *,
    run_date: date | None = None,
    find_code: bool = True,
    session: requests.Session | None = None,
    now: datetime | None = None,
    log=print,
) -> tuple[list[Paper], Path]:
    session = session or requests.Session()
    run_date = run_date or datetime.now(timezone.utc).date()

    log(f"Fetching candidates from arXiv: {', '.join(config.categories)}")
    candidates = arxiv.fetch_recent(
        config.categories,
        config.lookback_days,
        config.max_candidates,
        session=session,
        now=now,
    )
    log(f"  {len(candidates)} candidates in the last {config.lookback_days} day(s)")

    top = ranking.rank(candidates, config.topics, config.max_papers)
    log(f"Ranked -> {len(top)} paper(s) above threshold")

    provider = summarizer.detect_provider(config.llm)
    log(f"LLM provider: {provider}")

    for i, paper in enumerate(top, 1):
        log(f"  [{i}/{len(top)}] {paper.title[:70]}...")
        if find_code:
            paper.code_repos = code_finder.find_code(paper, session=session)
            if paper.code_repos:
                log(f"      found {len(paper.code_repos)} code repo(s)")
        paper.walkthrough = summarizer.summarize(paper, config.roles, config.llm)

    content = digest.render_digest(top, run_date, config.roles)
    path = digest.write_digest(content, config.output_dir, run_date)
    log(f"Wrote digest -> {path}")
    return top, path
