"""Persona = identity of an instance inside the Nexus framework."""

from typing import Literal

from pydantic import BaseModel, Field

PersonaKind = Literal[
    "personal", "family", "company", "community", "client", "custom",
]


class PersonaConfig(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=100)
    kind: PersonaKind = "personal"
    description: str = Field("", max_length=500)
    default_locale: str = Field("es-ES", pattern=r"^[a-z]{2}-[A-Z]{2}$")
