from datetime import datetime, timezone

from research_digest.sources import arxiv

SAMPLE_FEED = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2501.12345v1</id>
    <updated>2026-07-01T10:00:00Z</updated>
    <published>2026-07-01T09:00:00Z</published>
    <title>A Multi-Agent LLM Framework</title>
    <summary>We introduce an agentic system. Code at https://github.com/acme/agent-fw.</summary>
    <author><name>Jane Doe</name></author>
    <author><name>John Roe</name></author>
    <link href="http://arxiv.org/abs/2501.12345v1" rel="alternate" type="text/html"/>
    <link title="pdf" href="http://arxiv.org/pdf/2501.12345v1" rel="related" type="application/pdf"/>
    <category term="cs.AI"/>
    <category term="cs.MA"/>
  </entry>
</feed>
"""


class _FakeResp:
    status_code = 200
    text = SAMPLE_FEED

    def raise_for_status(self):
        return None


class _FakeSession:
    def get(self, *args, **kwargs):
        return _FakeResp()


def test_fetch_recent_parses_entry():
    now = datetime(2026, 7, 2, tzinfo=timezone.utc)
    papers = arxiv.fetch_recent(
        ["cs.AI"], lookback_days=3, session=_FakeSession(), now=now
    )
    assert len(papers) == 1
    p = papers[0]
    assert p.title == "A Multi-Agent LLM Framework"
    assert p.paper_id == "2501.12345v1"
    assert p.short_id == "2501.12345"
    assert p.authors == ["Jane Doe", "John Roe"]
    assert "cs.AI" in p.categories and "cs.MA" in p.categories
    assert p.pdf_url.endswith(".pdf") or "pdf" in p.pdf_url


def test_fetch_recent_filters_by_cutoff():
    now = datetime(2026, 7, 10, tzinfo=timezone.utc)
    papers = arxiv.fetch_recent(
        ["cs.AI"], lookback_days=1, session=_FakeSession(), now=now
    )
    assert papers == []
