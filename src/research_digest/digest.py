"""Assemble ranked, summarized papers into a Markdown digest file."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import Paper


def render_digest(papers: list[Paper], run_date: date, roles: list[str]) -> str:
    lines: list[str] = []
    lines.append(f"# Research Digest — {run_date.isoformat()}")
    lines.append("")
    roles_str = ", ".join(roles) if roles else "AI/data practitioners"
    lines.append(f"Curated for: **{roles_str}**")
    lines.append("")
    if not papers:
        lines.append("_No relevant papers matched today's filters._")
        return "\n".join(lines) + "\n"

    lines.append(f"**{len(papers)} paper(s)** made the cut today.")
    lines.append("")
    lines.append("## Table of contents")
    for i, paper in enumerate(papers, 1):
        anchor = f"{i}-{paper.short_id.replace('.', '')}"
        lines.append(f"{i}. [{paper.title}](#{anchor}) — score {paper.score:.1f}")
    lines.append("")

    for i, paper in enumerate(papers, 1):
        anchor = f"{i}-{paper.short_id.replace('.', '')}"
        lines.append(f'<a id="{anchor}"></a>')
        lines.append(f"## {i}. {paper.title}")
        lines.append("")
        authors = ", ".join(paper.authors[:6])
        if len(paper.authors) > 6:
            authors += " et al."
        lines.append(f"- **Authors:** {authors}")
        lines.append(f"- **Published:** {paper.published.date().isoformat()}")
        lines.append(f"- **Categories:** {', '.join(paper.categories)}")
        lines.append(f"- **arXiv:** [{paper.short_id}]({paper.abstract_url}) · [PDF]({paper.pdf_url})")
        matched = ", ".join(paper.matched_topics.keys())
        if matched:
            lines.append(f"- **Matched topics:** {matched}")
        if paper.code_repos:
            repo_links = ", ".join(f"[{r.url.split('github.com/')[-1]}]({r.url})" for r in paper.code_repos)
            lines.append(f"- **Code:** {repo_links}")
        lines.append("")
        lines.append(paper.walkthrough or "_No walkthrough generated._")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines) + "\n"


def write_digest(content: str, output_dir: str | Path, run_date: date) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{run_date.isoformat()}.md"
    path.write_text(content, encoding="utf-8")
    _update_index(output_dir)
    return path


def _update_index(output_dir: Path) -> None:
    digests = sorted(
        (p for p in output_dir.glob("*.md") if p.name != "README.md"),
        reverse=True,
    )
    lines = ["# Digest archive", ""]
    for p in digests:
        lines.append(f"- [{p.stem}]({p.name})")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
