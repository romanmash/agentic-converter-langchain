"""LangChain model factory."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from src.config.manager import AppConfig, LLMParameters


def create_chat_model(config: AppConfig, llm_params: LLMParameters) -> ChatOpenAI:
    """Create a configured ``ChatOpenAI`` model for a specific agent."""

    return ChatOpenAI(
        model=config.llm.model,
        api_key=config.llm.api_key,
        base_url=config.llm.base_url,
        temperature=llm_params.temperature,
        max_tokens=llm_params.max_tokens,
        top_p=llm_params.top_p,
        extra_body={"top_k": llm_params.top_k},
    )
