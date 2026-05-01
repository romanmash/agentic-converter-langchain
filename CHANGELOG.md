# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Moved versioned demo input/output artifacts from `.data/` to `docs/data-demo/`
- Switched `.data/input` and `.data/output` to `.gitkeep`-only tracking
- Refined README, `docs/PITCH.md`, `CONTRIBUTING.md`, and `AGENTS.md` to match the new runtime-vs-demo data layout

## [1.0.1] - 2026-03-09

### Fixed

- Suppressed the LangChain Core Pydantic v1 warning on Python 3.14+ to keep CLI output clean
- Sanitized report iteration comments to remove markdown fence lines like ` ``` ` from table cells

### Changed

- Bumped project version metadata to `1.0.1`

## [1.0.0] - 2026-03-07

### Added

- Full converter-reviewer parity flow with iteration history tracking
- Markdown conversion report generation (`report.md`) with confidence and checklist
- `.data/input/2/Jenkinsfile` sample for batch demos
- Expanded README and `docs/PITCH.md` with architecture diagrams and explanations

### Changed

- CLI now writes both `ci.yml` and `report.md` for each converted file
- End-of-run summary output now mirrors main project style
