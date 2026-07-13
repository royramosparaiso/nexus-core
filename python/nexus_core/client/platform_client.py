"""Typed HTTP client that Console uses to talk to a running Platform.

Every command is wrapped in a signed JWT envelope. The client also verifies
that Platform's response is well-formed. Notification verification (the reverse
direction) lives in a separate helper — see verify_incoming_notification.
"""

from __future__ import annotations

import time
from uuid import UUID, uuid4

import httpx

from nexus_core.contracts.bootstrap import BootstrapRequest, BootstrapResponse
from nexus_core.contracts.commands import (
    Command, CommandEnvelope, CommandResult,
)
from nexus_core.contracts.notifications import NotificationEnvelope
from nexus_core.jwt.keys import ConsoleKeypair
from nexus_core.jwt.sign import (
    DEFAULT_LIFETIME_SECONDS, sign_command, verify_token,
)


class PlatformClientError(Exception):
    pass


class PlatformClient:
    """Sync HTTP client — Console → Platform.

    Async version can be added later using httpx.AsyncClient; interface stays
    the same.
    """

    def __init__(
        self,
        base_url: str,
        console_keypair: ConsoleKeypair,
        instance_id: UUID,
        *,
        platform_public_pem: str | None = None,
        timeout_s: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._kp = console_keypair
        self._instance_id = instance_id
        self._platform_pub = platform_public_pem
        self._client = httpx.Client(timeout=timeout_s)

    def close(self) -> None:
        self._client.close()

    # ---- bootstrap -------------------------------------------------------

    def bootstrap(
        self, request: BootstrapRequest, bootstrap_token: str,
    ) -> BootstrapResponse:
        """One-time /_bootstrap call. Uses BOOTSTRAP_TOKEN, not JWT."""
        r = self._client.post(
            f"{self._base_url}/_bootstrap",
            json=request.model_dump(mode="json"),
            headers={"X-Bootstrap-Token": bootstrap_token},
        )
        if r.status_code >= 500:
            raise PlatformClientError(f"platform 5xx: {r.status_code} {r.text}")
        try:
            data = r.json()
        except ValueError as exc:
            raise PlatformClientError("non-json response") from exc
        resp = BootstrapResponse.model_validate(data)
        if resp.platform_public_key_pem:
            self._platform_pub = resp.platform_public_key_pem
        return resp

    # ---- commands --------------------------------------------------------

    def send_command(
        self, command: Command, *, lifetime_s: int = DEFAULT_LIFETIME_SECONDS,
    ) -> CommandResult:
        now = int(time.time())
        env = CommandEnvelope(
            cmd_id=uuid4(),
            instance_id=self._instance_id,
            issued_at=now,
            expires_at=now + lifetime_s,
            command=command,
        )
        token = sign_command(self._kp, env)
        r = self._client.post(
            f"{self._base_url}/_commands",
            content=token,
            headers={"Content-Type": "application/jwt"},
        )
        if r.status_code >= 500:
            raise PlatformClientError(f"platform 5xx: {r.status_code} {r.text}")
        try:
            data = r.json()
        except ValueError as exc:
            raise PlatformClientError("non-json response") from exc
        return CommandResult.model_validate(data)

    # ---- notification verification (Platform → Console webhook) ----------

    def verify_incoming_notification(self, jwt_token: str) -> NotificationEnvelope:
        if not self._platform_pub:
            raise PlatformClientError(
                "platform public key unknown — call bootstrap() first",
            )
        payload = verify_token(jwt_token, self._platform_pub)
        return NotificationEnvelope.model_validate(payload)
