"""Console↔Platform protocol contracts."""

from nexus_core.contracts.commands import (
    Command, CommandKind, CommandEnvelope,
    CommandResult, CommandStatus,
)
from nexus_core.contracts.notifications import (
    Notification, NotificationKind, NotificationEnvelope,
)
from nexus_core.contracts.bootstrap import (
    BootstrapRequest, BootstrapResponse, BootstrapStatus,
)

__all__ = [
    "Command", "CommandKind", "CommandEnvelope",
    "CommandResult", "CommandStatus",
    "Notification", "NotificationKind", "NotificationEnvelope",
    "BootstrapRequest", "BootstrapResponse", "BootstrapStatus",
]
