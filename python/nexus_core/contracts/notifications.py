"""Platform → Console notifications.

Sent by Platform to Console webhook. Signed with Platform private key; Console
verifies with the Platform public key it received at /_bootstrap response.
"""

from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NotificationKind(str, Enum):
    HEALTH_HEARTBEAT = "health_heartbeat"
    STATUS_CHANGED = "status_changed"
    AGENT_TRIGGERED_KILL_SWITCH = "agent_triggered_kill_switch"
    BUDGET_ALERT = "budget_alert"
    AUDIT_EVENT = "audit_event"
    ERROR = "error"


class Notification(BaseModel):
    kind: NotificationKind
    payload: dict[str, Any] = Field(default_factory=dict)


class NotificationEnvelope(BaseModel):
    notif_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    emitted_at: int
    notification: Notification
