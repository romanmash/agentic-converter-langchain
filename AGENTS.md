# AGENTS

Guidelines for coding assistants in this repository.

1. Keep architecture clean: I/O in `src/main.py`, domain logic in `src/*` modules.
2. Read prompts from `src/prompts/*.md`; do not hardcode system prompts.
3. Use config from `config/config.json` and optional `config/config.local.json`.
4. Prefer dependency injection over global client instances.
5. Preserve report format in `src/report/generator.py` when changing pipeline state/history.
6. Keep versioned demo Jenkinsfiles in `docs/data-demo/input/1` and `docs/data-demo/input/2`; keep `.data/input` and `.data/output` tracked only with `.gitkeep` placeholders.
