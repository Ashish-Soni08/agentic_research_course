"""Turn a paper (plus any code) into a technical walkthrough.

An LLM provider is auto-detected from the environment:
- OPENAI_API_KEY    -> OpenAI chat completions
- ANTHROPIC_API_KEY -> Anthropic messages
- GEMINI_API_KEY    -> Google Gemini generateContent

If no key is available, an offline extractive summary is produced instead so the
pipeline always yields a useful digest and stays testable without credentials.
"""

from __future__ import annotations

import os
import textwrap

import requests

from .config import LLMConfig
from .models import Paper

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-1.5-flash",
}


def detect_provider(cfg: LLMConfig) -> str:
    if cfg.provider and cfg.provider != "auto":
        return cfg.provider
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    return "none"


def _build_prompt(paper: Paper, roles: list[str]) -> str:
    roles_str = ", ".join(roles) if roles else "a technical practitioner"
    code_block = ""
    for repo in paper.code_repos:
        code_block += f"\n- {repo.url}"
        if repo.stars is not None:
            code_block += f" (★{repo.stars})"
        if repo.description:
            code_block += f" — {repo.description}"
        if repo.readme_excerpt:
            code_block += f"\n  README excerpt:\n{textwrap.indent(repo.readme_excerpt[:1200], '    ')}"
    if not code_block:
        code_block = "\n(No public code repository was found automatically.)"

    return textwrap.dedent(
        f"""
        You are a senior AI research engineer writing a morning briefing for {roles_str}.
        Read the paper below and write a concise, high-signal technical walkthrough in
        Markdown. Do not invent results that are not supported by the abstract.

        Use exactly these sections (as Markdown H3 headings):
        ### TL;DR
        (2-3 sentences.)
        ### Why it matters for these roles
        (Bullets tying the work to {roles_str}.)
        ### Key technical takeaways
        (Bullets a technical person should definitely know.)
        ### Method & implementation
        (How it works, the core algorithm/architecture, at a technical level.)
        ### Code & how to use it
        (If a repo is provided, explain how to get started and the key entry points.
        If no repo was found, say so and describe how you would implement the core idea.)
        ### How to apply it in a product
        (Concrete ideas for using this in real apps/products.)

        TITLE: {paper.title}
        AUTHORS: {", ".join(paper.authors[:8])}
        CATEGORIES: {", ".join(paper.categories)}
        ABSTRACT:
        {paper.abstract}

        CODE REPOSITORIES:{code_block}
        """
    ).strip()


def _call_openai(prompt: str, cfg: LLMConfig, model: str) -> str:
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_output_tokens,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _call_anthropic(prompt: str, cfg: LLMConfig, model: str) -> str:
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": model,
            "max_tokens": cfg.max_output_tokens,
            "temperature": cfg.temperature,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    parts = resp.json().get("content", [])
    return "".join(p.get("text", "") for p in parts).strip()


def _call_gemini(prompt: str, cfg: LLMConfig, model: str) -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ["GOOGLE_API_KEY"]
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        params={"key": key},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": cfg.temperature,
                "maxOutputTokens": cfg.max_output_tokens,
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    candidates = resp.json().get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts).strip()


def _offline_summary(paper: Paper, roles: list[str]) -> str:
    roles_str = ", ".join(roles) if roles else "technical practitioners"
    topics = ", ".join(paper.matched_topics.keys()) or "n/a"
    if paper.code_repos:
        code_lines = []
        for repo in paper.code_repos:
            star = f" (★{repo.stars})" if repo.stars is not None else ""
            desc = f" — {repo.description}" if repo.description else ""
            code_lines.append(f"- [{repo.url}]({repo.url}){star}{desc}")
        code_section = "\n".join(code_lines)
    else:
        code_section = "_No public code repository found automatically._"

    return textwrap.dedent(
        f"""
        > **Offline summary** — no LLM API key configured, so this is an extractive
        > summary. Set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY`
        > for a full AI-written walkthrough.

        ### TL;DR
        {paper.abstract[:500]}{"..." if len(paper.abstract) > 500 else ""}

        ### Why it matters for these roles
        Relevant to {roles_str}. Matched topics: **{topics}**.

        ### Key technical takeaways
        {paper.abstract}

        ### Code & how to use it
        {code_section}
        """
    ).strip()


def summarize(paper: Paper, roles: list[str], cfg: LLMConfig) -> str:
    provider = detect_provider(cfg)
    if provider == "none":
        return _offline_summary(paper, roles)

    model = cfg.model or DEFAULT_MODELS.get(provider, "")
    prompt = _build_prompt(paper, roles)
    try:
        if provider == "openai":
            return _call_openai(prompt, cfg, model)
        if provider == "anthropic":
            return _call_anthropic(prompt, cfg, model)
        if provider == "gemini":
            return _call_gemini(prompt, cfg, model)
    except (requests.RequestException, KeyError, ValueError) as exc:
        return (
            f"> **LLM call failed** ({provider}: {exc}). Falling back to offline summary.\n\n"
            + _offline_summary(paper, roles)
        )
    return _offline_summary(paper, roles)
