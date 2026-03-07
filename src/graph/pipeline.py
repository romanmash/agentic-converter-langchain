from __future__ import annotations

from enum import Enum
from typing import Callable

from pydantic import BaseModel, Field

if False:  # pragma: no cover
    from langchain_openai import ChatOpenAI


class PipelineStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    CHANGES_NEEDED = "changes_needed"
    MAX_ITERATIONS = "max_iterations"
    ERROR = "error"


class IterationRecord(BaseModel):
    iteration: int
    action: str
    result: str
    comment: str = ""


class PipelineState(BaseModel):
    jenkinsfile: str
    workflow_yaml: str = ""
    review_feedback: str | None = None
    iteration: int = Field(default=0, ge=0)
    status: PipelineStatus = PipelineStatus.PENDING
    history: list[IterationRecord] = Field(default_factory=list)


def run_pipeline(
    jenkinsfile: str,
    converter_model: "ChatOpenAI",
    reviewer_model: "ChatOpenAI",
    converter_prompt: str,
    reviewer_prompt: str,
    max_iterations: int = 5,
    progress_callback: Callable[[str], None] | None = None,
) -> PipelineState:
    from src.agents.converter import convert
    from src.agents.reviewer import review

    state = PipelineState(jenkinsfile=jenkinsfile)
    for i in range(max_iterations):
        if progress_callback:
            progress_callback(f"Iteration {i + 1}/{max_iterations}: converting")
        state = convert(state=state, model=converter_model, system_prompt=converter_prompt)
        state = state.model_copy(
            update={
                "history": state.history
                + [
                    IterationRecord(
                        iteration=state.iteration,
                        action="convert",
                        result="Generated YAML" if state.iteration == 1 else "Applied reviewer feedback",
                    )
                ]
            }
        )

        if progress_callback:
            progress_callback(f"Iteration {i + 1}/{max_iterations}: reviewing")
        state = review(state=state, model=reviewer_model, system_prompt=reviewer_prompt)
        is_approved = state.status == PipelineStatus.APPROVED
        state = state.model_copy(
            update={
                "history": state.history
                + [
                    IterationRecord(
                        iteration=state.iteration,
                        action="review",
                        result="APPROVED" if is_approved else "CHANGES NEEDED",
                        comment=state.review_feedback.strip() if state.review_feedback else "",
                    )
                ]
            }
        )

        if state.status == PipelineStatus.APPROVED:
            return state
        if progress_callback and state.review_feedback:
            progress_callback(f"Reviewer feedback:\n{state.review_feedback}")

    return state.model_copy(update={"status": PipelineStatus.MAX_ITERATIONS})
