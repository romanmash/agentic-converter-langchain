# Contributing to Agentic Converter LC

## Project Principles

These principles govern implementation and reviews:

1. **Local-first execution**: The application targets a local OpenAI-compatible endpoint.
2. **Clean boundaries**: Keep I/O in `src/main.py`; agents and report generation stay pure.
3. **Configuration over hardcoding**: Runtime defaults come from `config/config.json`, optional machine-local overrides come from `config/config.local.json`, and CLI wins per run. Package version comes only from `pyproject.toml`.
4. **Deterministic reporting**: Preserve report structure and state history behavior in `src/report/generator.py`.
5. **Practical minimalism**: Prefer the smallest correct change over speculative abstraction.

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `chore` | Build process, tooling, dependencies |

### Examples

```
feat(cli): add --version flag reading from pyproject.toml
fix(converter): handle empty LLM response with retry
docs: align README with data-demo runtime policy
chore: tune langchain-openai dependency range
```

## Development Workflow

1. **Read** the Project Principles section in this file.
2. **Check** `specs/001-langchain-converter/tasks.md` for current work items.
3. **Implement** following the plan in `specs/001-langchain-converter/plan.md`.
4. **Validate** by running the CLI with local sample input.
5. **Commit** using conventional commit format.

## Setup

```bash
uv sync
cp config/config.local.example.json config/config.local.json  # Optional local overrides
uv run python -m src.main --help
uv run python -m src.main .data/input/ -v
```

## Pull Request Checklist

- [ ] No hardcoded runtime values (`config/config.json` / `config/config.local.json` / CLI only)
- [ ] I/O only in `src/main.py`
- [ ] Conventional commit message
- [ ] `CHANGELOG.md` updated (if user-facing change)
- [ ] If tests were added/changed, include exact commands and results
