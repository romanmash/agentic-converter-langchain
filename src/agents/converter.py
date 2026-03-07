from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.graph.pipeline import PipelineState, PipelineStatus

if False:  # pragma: no cover
    from langchain_openai import ChatOpenAI


def _strip_yaml_fences(text: str) -> str:
    output = text.strip()
    if output.startswith("```yaml"):
        output = output[7:]
    if output.startswith("```"):
        output = output[3:]
    if output.endswith("```"):
        output = output[:-3]
    return output.strip()


def convert(
    state: PipelineState,
    model: "ChatOpenAI",
    system_prompt: str,
) -> PipelineState:
    if state.iteration == 0:
        converter_input = (
            "Convert this Jenkinsfile to a complete GitHub Actions workflow YAML.\n\n"
            f"```groovy\n{state.jenkinsfile}\n```"
        )
    else:
        converter_input = (
            "Revise your previous YAML using reviewer feedback. Return full corrected YAML only.\n\n"
            f"Reviewer feedback:\n{state.review_feedback}\n\n"
            f"Original Jenkinsfile:\n```groovy\n{state.jenkinsfile}\n```\n\n"
            f"Previous YAML:\n```yaml\n{state.workflow_yaml}\n```"
        )

    prompt = ChatPromptTemplate.from_messages([("system", "{system_prompt}"), ("human", "{converter_input}")])
    chain = prompt | model | StrOutputParser()

    raw_output = chain.invoke({"system_prompt": system_prompt, "converter_input": converter_input})
    yaml_output = _strip_yaml_fences(raw_output)
    if not yaml_output:
        raise ValueError("converter returned empty content")

    return state.model_copy(
        update={"workflow_yaml": yaml_output, "iteration": state.iteration + 1, "status": PipelineStatus.IN_PROGRESS}
    )
