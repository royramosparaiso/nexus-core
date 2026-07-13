"""Console → Platform commands.

Every command is wrapped in a signed JWT envelope. The Platform verifies the
signature with the Console public key (delivered at /_bootstrap).
"""

from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CommandKind(str, Enum):
    # LLM / provider
    SET_LLM_PROVIDER = "set_llm_provider"
    ROTATE_SECRET = "rotate_secret"

    # Area / agent lifecycle
    INSTALL_AREA = "install_area"
    UNINSTALL_AREA = "uninstall_area"
    DEPLOY_AGENT = "deploy_agent"
    UPDATE_CEILING = "update_ceiling"
    KILL_SWITCH_AGENT = "kill_switch_agent"

    # Space lifecycle
    CREATE_SPACE = "create_space"
    DELETE_SPACE = "delete_space"
    GRANT_CROSS_INSTANCE_ACCESS = "grant_cross_instance_access"

    # Platform lifecycle
    UPGRADE_PLATFORM = "upgrade_platform"
    PAUSE = "pause"
    RESUME = "resume"


class Command(BaseModel):
    kind: CommandKind
    payload: dict[str, Any] = Field(default_factory=dict)


class CommandEnvelope(BaseModel):
    """Signed envelope. The whole envelope is the JWT payload."""

    cmd_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    issued_at: int  # epoch seconds
    expires_at: int  # epoch seconds
    command: Command


class CommandStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    APPLIED = "applied"
    FAILED = "failed"
    REJECTED = "rejected"


class CommandResult(BaseModel):
    cmd_id: UUID
    status: CommandStatus
    detail: str | None = None
    applied_at: int | None = None  # epoch seconds
    error_code: str | None = None
