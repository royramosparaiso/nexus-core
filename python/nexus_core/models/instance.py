"""Instance manifest = payload delivered by Console to Platform on /_bootstrap."""

from typing import Literal

from pydantic import BaseModel, Field

from nexus_core.models.areas import AreasConfig
from nexus_core.models.deployment import DeploymentConfig
from nexus_core.models.governance import GovernanceConfig
from nexus_core.models.llm import LlmConfig
from nexus_core.models.memory import MemoryConfig
from nexus_core.models.persona import PersonaConfig

InstanceStatus = Literal[
    "bootstrap-pending",   # created in Console, not yet ACKed by Platform
    "bootstrapping",       # Platform received manifest, applying it
    "running",             # healthy
    "degraded",            # partial outage
    "paused",              # kill-switch or operator pause
    "error",               # failed bootstrap
]


class InstanceManifest(BaseModel):
    """The nexus.instance.yaml payload as a typed object.

    Console emits this. Platform receives it at /_bootstrap. Both sides use the
    same class to eliminate schema drift.
    """

    api_version: Literal["nexus.v0.6"] = Field("nexus.v0.6", alias="apiVersion")
    kind: Literal["Instance"] = "Instance"
    name: str = Field(..., min_length=1, max_length=100)
    persona: PersonaConfig
    deployment: DeploymentConfig
    llms: LlmConfig
    memory: MemoryConfig
    areas: AreasConfig
    governance: GovernanceConfig

    model_config = {"populate_by_name": True}
