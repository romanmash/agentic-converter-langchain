from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.graph.pipeline import PipelineState, PipelineStatus

if False:  # pragma: no cover
    from langchain_openai import ChatOpenAI


def _parse_verdict(response: str) -> tuple[PipelineStatus, str | None]:
    cleaned = response.strip()
    for line in cleaned.splitlines():
        line_u = line.strip().upper()
        if not line_u.startswith("STATUS:"):
            continue

        status_value = line_u.split(":", 1)[1].strip()
        if status_value == "APPROVED":
            return PipelineStatus.APPROVED, None

        if "CHANGES_NEEDED" in status_value or "CHANGES NEEDED" in status_value:
            feedback = cleaned[cleaned.find(line) + len(line) :].strip()
            return PipelineStatus.CHANGES_NEEDED, feedback or cleaned

    return PipelineStatus.CHANGES_NEEDED, cleaned


def review(
    state: PipelineState,
    model: "ChatOpenAI",
    system_prompt: str,
) -> PipelineState:
    reviewer_input = (
        "Review this Jenkinsfile conversion.\n\n"
        f"Original Jenkinsfile:\n```groovy\n{state.jenkinsfile}\n```\n\n"
        f"Generated GitHub Actions YAML:\n```yaml\n{state.workflow_yaml}\n```"
    )

    prompt = ChatPromptTemplate.from_messages([("system", "{system_prompt}"), ("human", "{reviewer_input}")])
    chain = prompt | model | StrOutputParser()

    response = chain.invoke({"system_prompt": system_prompt, "reviewer_input": reviewer_input})
    status, feedback = _parse_verdict(response)

    return state.model_copy(update={"status": status, "review_feedback": feedback})
