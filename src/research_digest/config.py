"""Load and validate the digest configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class LLMConfig:
    provider: str = "auto"
    model: str = ""
    temperature: float = 0.2
    max_output_tokens: int = 1200


@dataclass
class Config:
    categories: list[str] = field(default_factory=lambda: ["cs.AI", "cs.CL", "cs.LG"])
    lookback_days: int = 2
    max_papers: int = 8
    max_candidates: int = 120
    topics: dict[str, list[str]] = field(default_factory=dict)
    roles: list[str] = field(default_factory=list)
    llm: LLMConfig = field(default_factory=LLMConfig)
    output_dir: str = "digests"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        data = dict(data or {})
        llm_data = data.pop("llm", {}) or {}
        llm = LLMConfig(
            provider=str(llm_data.get("provider", "auto")),
            model=str(llm_data.get("model", "") or ""),
            temperature=float(llm_data.get("temperature", 0.2)),
            max_output_tokens=int(llm_data.get("max_output_tokens", 1200)),
        )
        return cls(
            categories=list(data.get("categories", ["cs.AI", "cs.CL", "cs.LG"])),
            lookback_days=int(data.get("lookback_days", 2)),
            max_papers=int(data.get("max_papers", 8)),
            max_candidates=int(data.get("max_candidates", 120)),
            topics=dict(data.get("topics", {})),
            roles=list(data.get("roles", [])),
            llm=llm,
            output_dir=str(data.get("output_dir", "digests")),
        )


def load_config(path: str | Path) -> Config:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return Config.from_dict(data)
