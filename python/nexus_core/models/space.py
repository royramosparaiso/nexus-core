"""Space = collaborative container inside an instance.

Replaces the previous 'Project Space' term from earlier v0.5 drafts.
"""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

SpaceKind = Literal[
    "internal", "company", "client", "community", "group", "family", "ad_hoc",
]


class SpaceRef(BaseModel):
    """Lightweight reference to a space — enough to route + audit."""

    space_id: UUID
    instance_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    kind: SpaceKind = "ad_hoc"
