"""Shared domain models — used by both Console and Platform."""

from nexus_core.models.persona import PersonaKind, PersonaConfig
from nexus_core.models.deployment import Modality, AgentRuntime, DeploymentConfig
from nexus_core.models.llm import LlmProvider, LlmRoleAssignment, LlmConfig
from nexus_core.models.memory import MemoryDriver, GraphDriver, MemoryConfig
from nexus_core.models.areas import Area, AreaTier, AreasConfig, AVAILABLE_AREAS
from nexus_core.models.governance import (
    AutonomyLevel, AuthProvider, AuthConfig, GovernanceConfig,
)
from nexus_core.models.instance import InstanceManifest, InstanceStatus
from nexus_core.models.space import SpaceKind, SpaceRef

__all__ = [
    "PersonaKind", "PersonaConfig",
    "Modality", "AgentRuntime", "DeploymentConfig",
    "LlmProvider", "LlmRoleAssignment", "LlmConfig",
    "MemoryDriver", "GraphDriver", "MemoryConfig",
    "Area", "AreaTier", "AreasConfig", "AVAILABLE_AREAS",
    "AutonomyLevel", "AuthProvider", "AuthConfig", "GovernanceConfig",
    "InstanceManifest", "InstanceStatus",
    "SpaceKind", "SpaceRef",
]
