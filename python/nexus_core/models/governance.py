"""Governance = autonomy ceilings + safety controls."""

from typing import Literal

from pydantic import BaseModel, Field

AutonomyLevel = Literal[
    "read_only", "propose", "act_with_approval", "act_autonomously",
]


class GovernanceConfig(BaseModel):
    default_autonomy: AutonomyLevel = "act_with_approval"
    kill_switch_enabled: bool = True
    audit_retention_days: int = Field(730, ge=90, le=3650)
    monthly_budget_alert_pct: int = Field(80, ge=10, le=100)
    require_2fa_for_superadmin: bool = True
