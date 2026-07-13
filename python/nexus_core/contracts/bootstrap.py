"""/_bootstrap — the very first exchange between Console and a fresh Platform.

Flow:
  1. Console deploys a Platform (docker / fly / k8s).
  2. Console POSTs BootstrapRequest to Platform's /_bootstrap endpoint using a
     one-time bootstrap token (BOOTSTRAP_TOKEN env var in the Platform).
  3. Platform stores the Console public key, generates its own keypair, applies
     the instance manifest, and returns BootstrapResponse with its public key +
     callback webhook URL for Console.
  4. From that moment, all commands and notifications are signed JWTs.
"""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from nexus_core.models.instance import InstanceManifest


class BootstrapStatus(str, Enum):
    OK = "ok"
    ALREADY_BOOTSTRAPPED = "already_bootstrapped"
    INVALID_TOKEN = "invalid_token"
    APPLY_FAILED = "apply_failed"


class BootstrapRequest(BaseModel):
    instance_id: UUID
    console_public_key_pem: str = Field(..., min_length=100)
    console_webhook_url: str = Field(..., pattern=r"^https?://")
    manifest: InstanceManifest


class BootstrapResponse(BaseModel):
    status: BootstrapStatus
    platform_public_key_pem: str | None = None
    platform_version: str | None = None
    applied_areas: list[str] = Field(default_factory=list)
    error_detail: str | None = None
