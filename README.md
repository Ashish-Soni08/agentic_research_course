# Agentic Research Course

This repository also hosts **`research-digest`**, a nightly agentic automation that
reads new papers for you before you wake up.

## What it does

Every night it:

1. **Fetches** the latest papers from arXiv (`cs.AI`, `cs.CL`, `cs.LG`, `cs.MA`, `cs.IR`).
2. **Ranks** them against the topics and roles you care about — AI agents, LLMs,
   multi-agent systems, AI automation, generative AI, data science — for roles like
   Data Analyst, Data Scientist, AI Engineer, LLM Engineer, Generative AI Engineer.
3. **Finds the code** that implements each paper (GitHub links in the abstract +
   Papers with Code), and pulls repo stars/description/README.
4. **Reads each paper with an LLM** and writes a technical walkthrough: TL;DR, why it
   matters for your roles, key takeaways, method & implementation, how to use the code,
   and how to apply it in a product.
5. **Writes a dated Markdown digest** to `digests/YYYY-MM-DD.md`.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run it now (writes digests/<today>.md)
research-digest run
```

Useful flags:

```bash
research-digest run --max-papers 5     # cap how many papers get summarized
research-digest run --no-code          # skip GitHub / Papers with Code lookups
research-digest run --date 2026-07-02  # override the run date
research-digest run -c config.yaml     # use a specific config file
```

## Configuration

Everything is controlled by [`config.yaml`](config.yaml): arXiv categories, lookback
window, topic keywords (which drive ranking), your target roles, and the LLM settings.

## LLM providers

The summarizer auto-detects a provider from the environment. Set one of:

| Env var | Provider | Default model |
| --- | --- | --- |
| `OPENAI_API_KEY` | OpenAI | `gpt-4o-mini` |
| `ANTHROPIC_API_KEY` | Anthropic | `claude-3-5-haiku-latest` |
| `GEMINI_API_KEY` | Google Gemini | `gemini-1.5-flash` |
| `HF_TOKEN` | Hugging Face (Inference Providers) | `meta-llama/Llama-3.1-8B-Instruct` |

If **no key** is set, an offline extractive summary is produced instead, so the pipeline
still works (just without the AI-written analysis).

### Using a Hugging Face token

Hugging Face is served through the OpenAI-compatible
[Inference Providers router](https://huggingface.co/docs/inference-providers) — one
`HF_TOKEN` gives access to many open models (Llama, Qwen, DeepSeek, gpt-oss, …).

1. Create a token at <https://huggingface.co/settings/tokens> with the
   **"Make calls to Inference Providers"** permission.
2. Export it (any of `HF_TOKEN`, `HUGGINGFACE_API_KEY`, `HUGGINGFACEHUB_API_TOKEN`):
   ```bash
   export HF_TOKEN=hf_xxx
   ```
3. Pick a model in `config.yaml`, e.g.:
   ```yaml
   llm:
     provider: huggingface
     model: "meta-llama/Llama-3.3-70B-Instruct"   # or Qwen/Qwen2.5-7B-Instruct, etc.
   ```
   Append `:groq` / `:together` / `:fastest` / `:cheapest` to the model to steer routing.

## Run it automatically every night

[`.github/workflows/nightly-digest.yml`](.github/workflows/nightly-digest.yml) runs the
pipeline on a nightly cron and commits the new digest back to the repo. Add your LLM key
as a repository secret (**Settings → Secrets and variables → Actions**) named
`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY`.

## Development

```bash
pip install -e ".[dev]"
pytest
```
