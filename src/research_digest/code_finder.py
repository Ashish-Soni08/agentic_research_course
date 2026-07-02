"""Find code that implements a paper.

Two strategies, both best-effort and fault tolerant:
1. Scrape GitHub URLs directly out of the abstract text.
2. Query the Papers with Code API by arXiv id.

When a GitHub repo is found we optionally enrich it with stars, description and a
README excerpt so the digest can explain how to actually use the code.
"""

from __future__ import annotations

import base64
import os
import re

import requests

from .models import CodeRepo, Paper

GITHUB_URL_RE = re.compile(r"https?://github\.com/[\w.\-]+/[\w.\-]+", re.IGNORECASE)
PWC_PAPER_API = "https://paperswithcode.com/api/v1/papers/"
USER_AGENT = "research-digest/0.1"


def _clean_repo_url(url: str) -> str:
    url = url.rstrip("/.,);]")
    # Normalize to owner/repo (strip deep paths like /tree/main).
    m = re.match(r"(https?://github\.com/[\w.\-]+/[\w.\-]+)", url, re.IGNORECASE)
    return m.group(1) if m else url


def _extract_from_abstract(paper: Paper) -> list[str]:
    found = GITHUB_URL_RE.findall(paper.abstract or "")
    return list(dict.fromkeys(_clean_repo_url(u) for u in found))


def _query_paperswithcode(paper: Paper, session: requests.Session) -> list[str]:
    urls: list[str] = []
    try:
        resp = session.get(
            PWC_PAPER_API,
            params={"arxiv_id": paper.short_id},
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        if resp.status_code != 200:
            return urls
        results = resp.json().get("results", [])
        if not results:
            return urls
        pwc_id = results[0].get("id")
        if not pwc_id:
            return urls
        repo_resp = session.get(
            f"{PWC_PAPER_API}{pwc_id}/repositories/",
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        if repo_resp.status_code != 200:
            return urls
        for repo in repo_resp.json().get("results", []):
            url = repo.get("url")
            if url:
                urls.append(_clean_repo_url(url))
    except (requests.RequestException, ValueError):
        return urls
    return urls


def _github_headers() -> dict[str, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _enrich_github(repo: CodeRepo, session: requests.Session) -> None:
    m = re.match(r"https?://github\.com/([\w.\-]+)/([\w.\-]+)", repo.url, re.IGNORECASE)
    if not m:
        return
    owner, name = m.group(1), m.group(2)
    try:
        meta = session.get(
            f"https://api.github.com/repos/{owner}/{name}",
            headers=_github_headers(),
            timeout=20,
        )
        if meta.status_code == 200:
            data = meta.json()
            repo.stars = data.get("stargazers_count")
            repo.description = data.get("description")
        readme = session.get(
            f"https://api.github.com/repos/{owner}/{name}/readme",
            headers=_github_headers(),
            timeout=20,
        )
        if readme.status_code == 200:
            content = readme.json().get("content", "")
            try:
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
                repo.readme_excerpt = decoded[:2000]
            except (ValueError, UnicodeDecodeError):
                pass
    except (requests.RequestException, ValueError):
        return


def find_code(
    paper: Paper,
    *,
    session: requests.Session | None = None,
    use_paperswithcode: bool = True,
    enrich: bool = True,
) -> list[CodeRepo]:
    session = session or requests.Session()

    repos: dict[str, CodeRepo] = {}
    for url in _extract_from_abstract(paper):
        repos[url.lower()] = CodeRepo(url=url, source="abstract")

    if use_paperswithcode:
        for url in _query_paperswithcode(paper, session):
            key = url.lower()
            if key not in repos:
                repos[key] = CodeRepo(url=url, source="paperswithcode")

    result = list(repos.values())
    if enrich:
        for repo in result:
            _enrich_github(repo, session)
    return result
