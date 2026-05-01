# Feature Specification: LangChain Agentic Converter

**Feature Branch**: `001-langchain-converter`
**Created**: 2026-03-06
**Status**: Draft
**Input**: User description: "Build a simplified LangChain-based variant that demonstrates the same converter↔reviewer agentic loop as the existing Agentic Converter, proving the approach is workable with LangChain."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Single File Conversion via LangChain (Priority: P1)

As a DevOps engineer, I want to convert a single Jenkinsfile to GitHub Actions YAML using a LangChain-based agentic loop so that I can evaluate LangChain as an alternative framework.

**Why this priority**: Core functionality — proves LangChain can orchestrate the same converter↔reviewer pattern.

**Independent Test**: Run `uv run python -m src.main .data/input/1/Jenkinsfile` and verify `.data/output/1/ci.yml` is created with valid YAML.

**Acceptance Scenarios**:

1. **Given** a valid Jenkinsfile at `.data/input/1/Jenkinsfile`, **When** I run the tool, **Then** `.data/output/1/ci.yml` is created with valid GitHub Actions YAML
2. **Given** LM Studio is not running, **When** I run the tool, **Then** I get a clear error message and exit code 1

---

### User Story 2 — Iterative Quality via LangChain Chains (Priority: P1)

As a DevOps engineer, I want the LangChain-based converter to iterate using a reviewer chain so that quality improves automatically across iterations.

**Why this priority**: The agentic loop is the core differentiator — demonstrates LangChain chain composition.

**Independent Test**: Run with `-v` flag and observe multi-iteration output with reviewer feedback.

**Acceptance Scenarios**:

1. **Given** a Jenkinsfile, **When** the reviewer approves on iteration 1, **Then** the loop terminates with status APPROVED
2. **Given** a Jenkinsfile, **When** the reviewer returns CHANGES_NEEDED, **Then** the converter re-runs with feedback
3. **Given** max iterations is 5, **When** the reviewer never approves, **Then** the loop stops at iteration 5

---

### Edge Cases

- What happens when LM Studio is unreachable? → Clear error message, exit code 1
- What happens when the LLM returns empty content? → Treat as error, log warning
- What happens when reviewer response is unparseable? → Treat as CHANGES_NEEDED

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use LangChain `ChatOpenAI` for LLM communication
- **FR-002**: System MUST implement converter and reviewer as LangChain chains
- **FR-003**: System MUST implement the converter↔reviewer loop with immutable state
- **FR-004**: System MUST accept a file path as CLI input
- **FR-005**: System MUST write generated YAML to output directory
- **FR-006**: System MUST load config from `config/config.json`
- **FR-007**: System MUST support `--version`, `--help`, `-v`, `-n`, `-o` CLI flags
- **FR-008**: System MUST read system prompts from `src/prompts/*.md` files
- **FR-009**: System MUST support separate LLM parameters for converter and reviewer

### Key Entities

- **PipelineState**: Core state model — `jenkinsfile`, `workflow_yaml`, `review_feedback`, `iteration`, `status`
- **AppConfig**: Configuration — `max_iterations`, `output_dir`, `verbose`, `llm` settings

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Jenkinsfile produces valid YAML that parses without errors
- **SC-002**: The agentic loop converges (APPROVED) or terminates at max iterations
- **SC-003**: LangChain `ChatOpenAI` and prompt templates are used throughout
- **SC-004**: Codebase is under 400 lines of application code
- **SC-005**: Architecture mirrors the original Agentic Converter design (Clean Architecture, DI, prompts-as-config)
