# AGENTS.md

## Cursor Cloud specific instructions

This repo contains two things:

1. **Course materials** — `.firecrawl/week-01.md` (scraped Week 1 content).
2. **`research-digest`** — a Python package (`src/research_digest/`) that runs a nightly
   agentic pipeline: fetch recent arXiv papers → rank by configured topics → find code →
   summarize each with an LLM → write `digests/YYYY-MM-DD.md`.

### Environment / running

- Python project using a `src/` layout. Install with `pip install -e ".[dev]"` inside a
  venv (`python3 -m venv .venv`). On this VM `python3-venv` must be present (apt package
  `python3.12-venv`); the update script installs it.
- Run the pipeline: `research-digest run` (see `README.md` for flags). Tests: `pytest`.
- There is **no server/daemon** — it is a batch job. "Running" it means executing
  `research-digest run`, which writes a Markdown file under `digests/`.

### Non-obvious notes

- **arXiv requires HTTPS** (`https://export.arxiv.org/...`); the plain-HTTP endpoint
  returns an empty body on this VM. `sources/arxiv.py` already uses HTTPS.
- The LLM step **auto-detects** a provider from `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` /
  `GEMINI_API_KEY` / `HF_TOKEN`. With **no key set it silently falls back** to an offline
  extractive summary, so a run "succeeding" does not prove the LLM path ran — check the
  `LLM provider:` line in the run log (it prints `none` when no key is configured).
- **Hugging Face** uses the OpenAI-compatible router `https://router.huggingface.co/v1`
  (`_call_huggingface`), auth via `HF_TOKEN`. Pick a chat model in `config.yaml`
  (`provider: huggingface`, `model: ...`); the token needs the "Make calls to Inference
  Providers" permission.
- Code discovery calls GitHub + Papers with Code; use `--no-code` to skip network calls
  to those services. A `GITHUB_TOKEN` (if present) raises GitHub API rate limits.
- The scheduled automation lives in `.github/workflows/nightly-digest.yml`; the LLM key
  must be added as a GitHub Actions repository secret for the nightly run to use a model.
