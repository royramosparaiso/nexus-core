"""LLM providers + router role assignments."""

from typing import Literal

from pydantic import BaseModel, Field

LlmProvider = Literal[
    "anthropic", "openai", "openrouter", "perplexity",
    "groq", "together", "mistral", "ollama",
]


class LlmRoleAssignment(BaseModel):
    planner: str
    coordinator: str
    worker: str
    embeddings: str


class LlmConfig(BaseModel):
    enabled_providers: list[LlmProvider] = Field(..., min_length=1)
    roles: LlmRoleAssignment
    allow_fallback: bool = True
    monthly_budget_usd: float = Field(50.0, ge=0)
