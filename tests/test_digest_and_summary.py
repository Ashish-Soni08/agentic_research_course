from datetime import date, datetime, timezone

from research_digest import summarizer
from research_digest.config import LLMConfig
from research_digest.digest import render_digest
from research_digest.models import CodeRepo, Paper


def _paper() -> Paper:
    now = datetime(2026, 7, 1, tzinfo=timezone.utc)
    p = Paper(
        source="arxiv",
        paper_id="2501.12345v1",
        title="A Multi-Agent LLM Framework",
        abstract="We introduce an agentic multi-agent system for automation.",
        authors=["Jane Doe"],
        categories=["cs.AI", "cs.MA"],
        published=now,
        updated=now,
        abstract_url="http://arxiv.org/abs/2501.12345v1",
        pdf_url="http://arxiv.org/pdf/2501.12345v1",
    )
    p.score = 9.0
    p.matched_topics = {"ai_agents": ["agentic"], "multi_agent_systems": ["multi-agent"]}
    p.code_repos = [CodeRepo(url="https://github.com/acme/agent-fw", source="abstract", stars=42)]
    return p


def test_offline_summary_used_without_key(monkeypatch):
    for var in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        monkeypatch.delenv(var, raising=False)
    cfg = LLMConfig(provider="auto")
    assert summarizer.detect_provider(cfg) == "none"
    text = summarizer.summarize(_paper(), ["Data Scientist"], cfg)
    assert "Offline summary" in text
    assert "### TL;DR" in text


def test_detect_provider_prefers_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "x")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "y")
    assert summarizer.detect_provider(LLMConfig(provider="auto")) == "openai"


class _FakeLLMResp:
    status_code = 200

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_openai_path_builds_request_and_parses(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    for var in ["ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        monkeypatch.delenv(var, raising=False)

    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["model"] = json["model"]
        captured["prompt"] = json["messages"][0]["content"]
        return _FakeLLMResp(
            {"choices": [{"message": {"content": "### TL;DR\nAI-written walkthrough."}}]}
        )

    monkeypatch.setattr(summarizer.requests, "post", fake_post)
    cfg = LLMConfig(provider="auto")
    out = summarizer.summarize(_paper(), ["AI Engineer"], cfg)

    assert out == "### TL;DR\nAI-written walkthrough."
    assert "openai.com" in captured["url"]
    assert captured["model"] == "gpt-4o-mini"
    # Prompt should include the paper title and the discovered code repo.
    assert "A Multi-Agent LLM Framework" in captured["prompt"]
    assert "github.com/acme/agent-fw" in captured["prompt"]


def test_llm_failure_falls_back_to_offline(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    def boom(*args, **kwargs):
        raise summarizer.requests.RequestException("network down")

    monkeypatch.setattr(summarizer.requests, "post", boom)
    out = summarizer.summarize(_paper(), ["AI Engineer"], LLMConfig(provider="auto"))
    assert "LLM call failed" in out
    assert "Offline summary" in out


def test_render_digest_contains_sections_and_links():
    p = _paper()
    p.walkthrough = "### TL;DR\nGreat paper."
    md = render_digest([p], date(2026, 7, 2), ["Data Scientist", "AI Engineer"])
    assert "# Research Digest — 2026-07-02" in md
    assert "A Multi-Agent LLM Framework" in md
    assert "github.com/acme/agent-fw" in md
    assert "Table of contents" in md
    assert "Great paper." in md


def test_render_digest_handles_no_papers():
    md = render_digest([], date(2026, 7, 2), ["Data Scientist"])
    assert "No relevant papers" in md
