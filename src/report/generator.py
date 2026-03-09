"""Conversion report generator."""

from __future__ import annotations

from datetime import datetime

from src.graph.pipeline import PipelineState, PipelineStatus

MANUAL_CHECKLIST: list[str] = [
    "**Secrets & Credentials** — Verify all `credentials()` / `withCredentials` blocks are replaced with GitHub Secrets (`${{ secrets.NAME }}`)",
    "**Custom Plugins** — Check for Jenkins plugin steps (SonarQube, Artifactory, etc.) that may need equivalent GitHub Actions",
    "**Shared Libraries** — Verify `@Library` imports are replaced with equivalent actions or composite workflows",
    "**Self-Hosted Runners** — Confirm `runs-on` labels match your GitHub runner infrastructure",
    "**Environment Variables** — Check dynamic `environment {}` blocks are correctly mapped to `env:` or `${{ vars.NAME }}`",
    "**Post-Build Actions** — Verify notifications (email, Slack, Jira) are handled via appropriate actions",
    "**Triggers** — Confirm `on:` triggers match original Jenkins trigger behavior (cron, pollSCM, upstream)",
    "**Artifacts & Workspace** — Verify `stash`/`unstash` replaced with `actions/upload-artifact` / `actions/download-artifact`",
    "**Parallel Execution** — Confirm parallel stages map to concurrent GHA jobs with correct `needs` dependencies",
    "**YAML Validity** — Run the generated workflow through a YAML linter or `actionlint`",
    "**Other** — Check for any other Jenkins-specific constructs not covered above",
]


def compute_confidence(status: PipelineStatus, iteration: int) -> str:
    if status == PipelineStatus.APPROVED and iteration <= 2:
        return "HIGH"
    if status == PipelineStatus.APPROVED and iteration <= 4:
        return "MEDIUM"
    return "LOW"


def _status_emoji(status: PipelineStatus) -> str:
    return {
        PipelineStatus.APPROVED: "✅",
        PipelineStatus.MAX_ITERATIONS: "⚠️",
        PipelineStatus.ERROR: "❌",
    }.get(status, "❓")


def _escape_table_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>")


def _sanitize_comment(value: str) -> str:
    lines = value.splitlines()
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Drop markdown fence-only lines so table comments never include dangling ```
        if stripped.startswith("```") and stripped.count("`") >= 3:
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def generate_report(
    state: PipelineState,
    source_path: str,
    output_path: str,
    max_iterations: int = 5,
) -> str:
    confidence = compute_confidence(state.status, state.iteration)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Conversion Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| **Source** | `{source_path}` |",
        f"| **Output** | `{output_path}` |",
        f"| **Status** | {_status_emoji(state.status)} {state.status.value.upper()} |",
        f"| **Iterations** | {state.iteration} / {max_iterations} |",
        f"| **Confidence** | {confidence} |",
        f"| **Generated** | {timestamp} |",
        "",
        "## Iteration History",
        "",
    ]

    if state.history:
        lines.extend(["| # | Action | Result | Comment |", "|---|---|---|---|"])
        for record in state.history:
            comment = _sanitize_comment(record.comment)
            lines.append(
                f"| {record.iteration} | {_escape_table_cell(record.action.capitalize())} | "
                f"{_escape_table_cell(record.result)} | {_escape_table_cell(comment)} |"
            )
    else:
        lines.append("*No iteration history recorded.*")

    lines.extend(
        [
            "",
            "## Manual Verification Checklist",
            "",
            "> Items below are common Jenkins→GHA conversion issues that",
            "> automated tools frequently miss. Review each relevant item.",
            "",
        ]
    )
    lines.extend([f"- [ ] {item}" for item in MANUAL_CHECKLIST])

    lines.extend(
        [
            "",
            "## Generated Workflow",
            "",
            "```yaml",
            state.workflow_yaml if state.workflow_yaml else "# No YAML generated",
            "```",
            "",
        ]
    )
    return "\n".join(lines)
