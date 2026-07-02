"""Core data structures shared across the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Paper:
    """A single paper pulled from an archive."""

    source: str
    paper_id: str
    title: str
    abstract: str
    authors: list[str]
    categories: list[str]
    published: datetime
    updated: datetime
    abstract_url: str
    pdf_url: str
    # Populated later in the pipeline.
    score: float = 0.0
    matched_topics: dict[str, list[str]] = field(default_factory=dict)
    code_repos: list["CodeRepo"] = field(default_factory=list)
    walkthrough: str | None = None

    @property
    def short_id(self) -> str:
        """arXiv id without version suffix, e.g. 2401.01234."""
        return self.paper_id.split("v")[0] if self.paper_id else self.paper_id


@dataclass
class CodeRepo:
    """A code repository associated with a paper."""

    url: str
    source: str  # e.g. "abstract" or "paperswithcode"
    stars: int | None = None
    description: str | None = None
    readme_excerpt: str | None = None
