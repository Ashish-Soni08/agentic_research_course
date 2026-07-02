"""Command line entry point for the research digest."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from .config import load_config
from .pipeline import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-digest",
        description="Fetch, rank and summarize recent papers into a Markdown digest.",
    )
    parser.add_argument(
        "command",
        choices=["run"],
        help="run: execute the full nightly pipeline.",
    )
    parser.add_argument(
        "-c", "--config", default="config.yaml", help="Path to config.yaml"
    )
    parser.add_argument(
        "--date", help="Override the run date (YYYY-MM-DD), defaults to today (UTC)."
    )
    parser.add_argument(
        "--no-code",
        action="store_true",
        help="Skip code/repository discovery (faster, no GitHub/PwC calls).",
    )
    parser.add_argument(
        "--max-papers", type=int, help="Override config max_papers for this run."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    if args.max_papers is not None:
        config.max_papers = args.max_papers

    run_date = date.fromisoformat(args.date) if args.date else None

    if args.command == "run":
        papers, path = run(config, run_date=run_date, find_code=not args.no_code)
        print(f"\nDone. {len(papers)} paper(s) summarized -> {path}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
