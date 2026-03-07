# Contributing

## Principles

1. Keep file I/O in `src/main.py`.
2. Keep agents and pipeline logic pure and testable.
3. Prefer configuration over hardcoded runtime values.
4. Keep report generation deterministic (`src/report/generator.py`).
5. Keep changes small and practical.

## Local Setup

```bash
uv sync
uv run python -m src.main --help
uv run python -m src.main .data/input/ -v
```
