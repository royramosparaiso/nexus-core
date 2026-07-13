"""Governance = autonomy ceilings + safety controls + auth provider.

See ADR-002 in nexus-platform for the auth provider taxonomy.
"""

from typing import Literal

from pydantic import BaseModel, Field

AutonomyLevel = Literal[
    "read_only", "propose", "act_with_approval", "act_autonomously",
]

AuthProvider = Literal[
    "password_totp",     # local password + TOTP; offline-friendly
    "magic_link",        # one-time signed email link (SMTP required)
    "oauth_google",      # Google Workspace / personal
    "oauth_microsoft",   # M365 / personal
    "oauth_github",      # developers
    "console_idp",       # Console signs user tokens; enables cross-instance
    "clerk",             # third-party auth-as-a-service (Clerk.com)
]


class AuthConfig(BaseModel):
    """Which auth provider serves this Platform's UI."""

    provider: AuthProvider = "password_totp"
    # Provider-specific credentials go through the Console credentials vault;
    # only their handles land here.
    smtp_credential_ref: str | None = None  # used when provider = magic_link
    oauth_credential_ref: str | None = None  # used when provider = oauth_*
    clerk_credential_ref: str | None = None  # used when provider = clerk


class GovernanceConfig(BaseModel):
    default_autonomy: AutonomyLevel = "act_with_approval"
    kill_switch_enabled: bool = True
    audit_retention_days: int = Field(730, ge=90, le=3650)
    monthly_budget_alert_pct: int = Field(80, ge=10, le=100)
    require_2fa_for_superadmin: bool = True
    auth: AuthConfig = Field(default_factory=AuthConfig)
