from datetime import datetime, timezone

from research_digest import code_finder
from research_digest.models import Paper


def _paper(abstract: str) -> Paper:
    now = datetime.now(timezone.utc)
    return Paper(
        source="arxiv",
        paper_id="2401.00001",
        title="t",
        abstract=abstract,
        authors=[],
        categories=["cs.AI"],
        published=now,
        updated=now,
        abstract_url="",
        pdf_url="",
    )


def test_extracts_github_url_from_abstract():
    p = _paper("Our code is available at https://github.com/acme/repo/tree/main.")
    repos = code_finder._extract_from_abstract(p)
    assert repos == ["https://github.com/acme/repo"]


def test_find_code_dedupes_and_no_network_when_disabled():
    p = _paper("See https://github.com/acme/repo and https://github.com/acme/repo.")
    repos = code_finder.find_code(
        p, use_paperswithcode=False, enrich=False
    )
    assert len(repos) == 1
    assert repos[0].url == "https://github.com/acme/repo"
    assert repos[0].source == "abstract"
