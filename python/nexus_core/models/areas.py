"""Available agent areas."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

AreaTier = Literal["core", "vertical"]


class Area(BaseModel):
    slug: str
    label: str
    tier: AreaTier
    default: bool


AVAILABLE_AREAS: list[Area] = [
    Area(slug="personal_organization", label="Personal organization", tier="core", default=True),
    Area(slug="meetings", label="Meetings & action items", tier="core", default=True),
    Area(slug="finance_personal", label="Personal finance", tier="core", default=True),
    Area(slug="comms", label="Communications", tier="core", default=True),
    Area(slug="brand", label="Brand & marketing", tier="vertical", default=False),
    Area(slug="sales", label="Sales & pipeline", tier="vertical", default=False),
    Area(slug="product", label="Product & roadmap", tier="vertical", default=False),
    Area(slug="dev", label="Dev (agent factory local)", tier="vertical", default=False),
    Area(slug="legal", label="Legal & compliance", tier="vertical", default=False),
    Area(slug="operations", label="Operations", tier="vertical", default=False),
]

_ALLOWED_SLUGS = {a.slug for a in AVAILABLE_AREAS}


class AreasConfig(BaseModel):
    enabled: list[str] = Field(..., min_length=1)

    @field_validator("enabled")
    @classmethod
    def _valid_slugs(cls, v: list[str]) -> list[str]:
        bad = [s for s in v if s not in _ALLOWED_SLUGS]
        if bad:
            raise ValueError(f"unknown area slugs: {bad}")
        return v
