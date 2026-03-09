"""LangChain Agentic Converter."""

from __future__ import annotations

import warnings

# LangChain currently imports a pydantic.v1 shim that emits this warning on Python 3.14+.
# Keep CLI output clean until upstream removes the v1 compatibility layer.
warnings.filterwarnings(
    "ignore",
    message=r"Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater\.",
    category=UserWarning,
    module=r"langchain_core\._api\.deprecation",
)
