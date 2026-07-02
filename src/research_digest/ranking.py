"""Score and rank papers against the topics you care about.

Scoring is deterministic and explainable so a nightly run is reproducible:
each topic keyword that appears in the title or abstract contributes points,
with title matches weighted higher.
"""

from __future__ import annotations

from .models import Paper

TITLE_WEIGHT = 3.0
ABSTRACT_WEIGHT = 1.0


def score_paper(paper: Paper, topics: dict[str, list[str]]) -> tuple[float, dict[str, list[str]]]:
    title = paper.title.lower()
    abstract = paper.abstract.lower()

    score = 0.0
    matched: dict[str, list[str]] = {}
    for topic, keywords in topics.items():
        hits: list[str] = []
        for kw in keywords:
            k = kw.lower().strip()
            if not k:
                continue
            in_title = k in title
            in_abstract = k in abstract
            if in_title:
                score += TITLE_WEIGHT
            if in_abstract:
                score += ABSTRACT_WEIGHT
            if in_title or in_abstract:
                hits.append(kw)
        if hits:
            # Reward papers that hit multiple distinct topics.
            matched[topic] = hits
    if len(matched) > 1:
        score += (len(matched) - 1) * 1.5
    return score, matched


def rank(papers: list[Paper], topics: dict[str, list[str]], max_papers: int) -> list[Paper]:
    for paper in papers:
        paper.score, paper.matched_topics = score_paper(paper, topics)
    ranked = sorted(papers, key=lambda p: (p.score, p.published), reverse=True)
    return [p for p in ranked if p.score > 0][:max_papers]
