from datetime import datetime, timezone

from research_digest.models import Paper
from research_digest.ranking import rank, score_paper

TOPICS = {
    "ai_agents": ["ai agent", "agentic", "multi-agent"],
    "llm": ["large language model", "llm"],
}


def _paper(title: str, abstract: str, pid: str = "2401.00001") -> Paper:
    now = datetime.now(timezone.utc)
    return Paper(
        source="arxiv",
        paper_id=pid,
        title=title,
        abstract=abstract,
        authors=["A. Author"],
        categories=["cs.AI"],
        published=now,
        updated=now,
        abstract_url="http://arxiv.org/abs/2401.00001",
        pdf_url="http://arxiv.org/pdf/2401.00001",
    )


def test_title_weighted_higher_than_abstract():
    p_title = _paper("An agentic LLM system", "unrelated body")
    p_abstract = _paper("Some system", "this uses an agentic large language model")
    s_title, _ = score_paper(p_title, TOPICS)
    s_abstract, _ = score_paper(p_abstract, TOPICS)
    assert s_title > s_abstract


def test_multi_topic_bonus_and_matched_topics():
    p = _paper("Multi-agent LLM agents", "agentic large language model orchestration")
    score, matched = score_paper(p, TOPICS)
    assert "ai_agents" in matched and "llm" in matched
    assert score > 0


def test_rank_filters_zero_score_and_limits():
    good = _paper("Agentic AI agent", "agentic", pid="2401.00002")
    irrelevant = _paper("A study of soil", "about farming", pid="2401.00003")
    ranked = rank([good, irrelevant], TOPICS, max_papers=5)
    assert [p.short_id for p in ranked] == ["2401.00002"]


def test_short_id_strips_version():
    assert _paper("t", "a", pid="2401.01234v3").short_id == "2401.01234"
