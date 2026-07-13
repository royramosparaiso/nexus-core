"""Memory + graph storage drivers."""

from typing import Literal

from pydantic import BaseModel, Field

MemoryDriver = Literal["sqlite", "postgres", "postgres_pgvector"]
GraphDriver = Literal["none", "neo4j", "postgres_graph"]


class MemoryConfig(BaseModel):
    driver: MemoryDriver = "postgres_pgvector"
    graph: GraphDriver = "none"
    retention_days: int = Field(365, ge=7, le=3650)
    encryption_at_rest: bool = True
