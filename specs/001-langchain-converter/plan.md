# Implementation Plan: LangChain Agentic Converter

**Branch**: `001-langchain-converter` | **Date**: 2026-03-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-langchain-converter/spec.md`

## Summary

Build a simplified CLI tool that converts Jenkinsfiles to GitHub Actions YAML using **LangChain** instead of raw `openai` SDK. The core architecture mirrors the existing Agentic Converter: a 2-agent iterative loop (converter↔reviewer) with immutable Pydantic state, Clean Architecture, and prompts stored as Markdown files. LangChain's `ChatOpenAI` and `ChatPromptTemplate` replace the direct OpenAI SDK calls. No tests required in this repository at this stage.

## Technical Context

**Language/Version**: Python 3.10+
**Package Manager**: uv
**Primary Dependencies**: langchain-openai (LLM communication via LangChain), pyyaml (YAML parsing), pydantic (data validation)
**Storage**: Local file system only
**Testing**: Not required in current repository scope
**Target Platform**: Any system running an OpenAI-compatible local proxy (e.g., LM Studio)
**Project Type**: CLI tool
**Constraints**: Local-only execution

## Constitution Check

*GATE: Must pass before implementation.*

- [x] Local-only execution? — Yes, LM Studio at localhost:1234
- [x] Clean Architecture? — DI for LLM, I/O only in main.py
- [x] No hardcoded values? — config/config.json, version in pyproject.toml
- [x] Simplicity? — LangChain used as minimal LLM wrapper, not over-engineered
- [x] Versioning? — pyproject.toml version field, CHANGELOG.md

## Project Structure

### Documentation (this feature)

```text
specs/001-langchain-converter/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py                  # CLI entry point — ALL I/O lives here
├── config/
│   ├── __init__.py
│   └── manager.py           # Config loading (config/config.json)
├── agents/
│   ├── __init__.py
│   ├── converter.py         # LangChain converter chain
│   └── reviewer.py          # LangChain reviewer chain
├── graph/
│   ├── __init__.py
│   └── pipeline.py          # PipelineState model + orchestration loop
├── llm/
│   ├── __init__.py
│   └── client.py            # LangChain ChatOpenAI wrapper
└── prompts/
    ├── converter.md          # Converter system prompt
    └── reviewer.md           # Reviewer system prompt

config/
├── config.json              # Default runtime configuration
└── config.local.example.json

pyproject.toml
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
AGENTS.md
.editorconfig
.gitignore

.data/                       # Working data (gitignored)
├── input/
│   └── 1/Jenkinsfile        # Sample Jenkinsfile
└── output/                  # Generated YAML

docs/
└── PITCH.md                 # Simplified pitch for LangChain variant
```

## Key Design Decisions

### LangChain as LLM Abstraction Layer

Replace the raw `openai.OpenAI` client with LangChain's `ChatOpenAI`. This demonstrates:
- **`ChatOpenAI`**: Drop-in replacement for OpenAI SDK, works with LM Studio
- **`ChatPromptTemplate`**: Structured prompt composition with system/user messages
- **Chain invocation**: Using LangChain's invoke pattern for cleaner agent calls

### What Changes from Original

| Aspect | Original (Raw Python) | LangChain Variant |
|---|---|---|
| LLM Client | `openai.OpenAI` | `langchain_openai.ChatOpenAI` |
| Prompt Building | String concatenation | `ChatPromptTemplate.from_messages()` |
| Agent Call | `client.chat(system, user, params)` | `chain.invoke({"input": ...})` |
| Dependencies | `openai` | `langchain-openai`, `langchain-core` |
| State Model | Pydantic (same) | Pydantic (same) |
| Pipeline Loop | Manual for-loop (same) | Manual for-loop (same) |
| Architecture | Clean Architecture (same) | Clean Architecture (same) |

### What Stays the Same

- Immutable `PipelineState` with `model_copy(update={...})`
- Converter↔reviewer loop in `pipeline.py`
- System prompts as Markdown files
- CLI with argparse
- Config from JSON file
- Clean Architecture (I/O boundary in `main.py`)

## Complexity Tracking

> No Constitution Check violations detected. No complexity justifications needed.
