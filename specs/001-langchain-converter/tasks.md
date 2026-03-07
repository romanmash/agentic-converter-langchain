# Tasks: LangChain Agentic Converter

**Input**: Design documents from `/specs/001-langchain-converter/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not included in current repository scope.

**Organization**: Tasks grouped by phase for sequential implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize project: create `pyproject.toml` with dependencies (langchain-openai, langchain-core, pyyaml, pydantic)
- [x] T002 Create directory structure: `src/config/`, `src/agents/`, `src/graph/`, `src/llm/`, `src/prompts/`, `docs/` with `__init__.py` files
- [x] T003 [P] Create `config/config.json` with runtime defaults
- [x] T004 [P] Create `config/config.local.example.json`
- [x] T005 [P] Create `.gitignore`, `.editorconfig`, `LICENSE`
- [x] T006 [P] Create sample `.data/input/1/Jenkinsfile`

---

## Phase 2: Core Implementation (US1 + US2)

**Purpose**: Configuration, LangChain client setup, agents, and pipeline

- [x] T007 Implement `src/config/manager.py`: `load_config()` reads `config/config.json`, returns Pydantic `AppConfig`
- [x] T008 Implement `src/llm/client.py`: `create_chat_model()` factory returning `ChatOpenAI` instance
- [x] T009 [P] Create `src/prompts/converter.md`: converter system prompt (reuse from original)
- [x] T010 [P] Create `src/prompts/reviewer.md`: reviewer system prompt (reuse from original)
- [x] T011 Implement `src/graph/pipeline.py`: `PipelineState` Pydantic model + `PipelineStatus` enum
- [x] T012 [US1] Implement `src/agents/converter.py`: LangChain chain using `ChatPromptTemplate` + `ChatOpenAI`
- [x] T013 [US2] Implement `src/agents/reviewer.py`: LangChain chain with verdict parsing
- [x] T014 [US2] Implement `run_pipeline()` in `src/graph/pipeline.py`: converter↔reviewer loop
- [x] T015 [US1] Implement `src/main.py`: CLI entry point with argparse, I/O boundary

---

## Phase 3: Documentation & Polish

**Purpose**: README, pitch, and project documentation

- [x] T016 Create `README.md` with Quick Start, CLI Reference, and architecture overview
- [x] T017 Create `CHANGELOG.md` with initial release
- [x] T018 Create `CONTRIBUTING.md` with project guidelines
- [x] T019 Create `AGENTS.md` with AI assistant instructions
- [x] T020 Create `docs/PITCH.md` — simplified pitch for LangChain variant

---

## Dependencies & Execution Order

- **Phase 1**: No dependencies — start immediately
- **Phase 2**: Depends on Phase 1
- **Phase 3**: Can run after Phase 2 core is done

## Implementation Strategy

1. Complete Phase 1 → Project scaffolded
2. Complete Phase 2 → Full implementation working
3. Complete Phase 3 → Documentation complete
