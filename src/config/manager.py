from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class LLMParameters(BaseModel):
    temperature: float
    max_tokens: int
    top_p: float
    top_k: int


class LLMConfig(BaseModel):
    base_url: str
    api_key: str
    model: str
    converter: LLMParameters
    reviewer: LLMParameters


class AppConfig(BaseModel):
    max_iterations: int = Field(ge=1, le=20)
    output_dir: str
    verbose: bool
    llm: LLMConfig


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path: Path | None = None) -> AppConfig:
    path = config_path or Path(__file__).resolve().parent.parent.parent / "config" / "config.json"
    if not path.exists():
        raise FileNotFoundError(f"config file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8-sig"))
    local_path = path.parent / "config.local.json"
    if local_path.exists():
        local_data = json.loads(local_path.read_text(encoding="utf-8-sig"))
        if isinstance(local_data, dict):
            data = _deep_merge(data, local_data)
    return AppConfig(**data)


def merge_with_cli(config: AppConfig, cli_args: dict[str, Any]) -> AppConfig:
    updates = {
        "output_dir": cli_args.get("output_dir"),
        "max_iterations": cli_args.get("max_iterations"),
        "verbose": cli_args.get("verbose"),
    }
    updates = {k: v for k, v in updates.items() if v is not None}
    return config.model_copy(update=updates) if updates else config


def load_project_version(pyproject_path: Path | None = None) -> str:
    path = pyproject_path or Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    if not path.exists():
        raise FileNotFoundError(f"pyproject.toml not found: {path}")

    in_project = False
    pattern = re.compile(r'^version\s*=\s*"([^"]+)"\s*$')
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue
        if in_project:
            match = pattern.match(stripped)
            if match:
                return match.group(1)
    raise ValueError("Could not find [project].version in pyproject.toml")
