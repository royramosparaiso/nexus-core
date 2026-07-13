"""JWT sign/verify helpers using EdDSA (Ed25519)."""

from __future__ import annotations

import time
from typing import Any

import jwt as pyjwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from nexus_core.contracts.commands import CommandEnvelope
from nexus_core.contracts.notifications import NotificationEnvelope
from nexus_core.jwt.errors import ExpiredToken, InvalidPayload, InvalidSignature
from nexus_core.jwt.keys import ConsoleKeypair, PlatformKeypair

ALGORITHM = "EdDSA"
DEFAULT_LIFETIME_SECONDS = 300  # 5 minutes


def _now() -> int:
    return int(time.time())


def _encode(payload: dict[str, Any], private_pem: str, kid: str) -> str:
    return pyjwt.encode(
        payload,
        private_pem,
        algorithm=ALGORITHM,
        headers={"kid": kid, "typ": "JWT"},
    )


def sign_command(
    kp: ConsoleKeypair,
    envelope: CommandEnvelope,
    kid: str = "console",
) -> str:
    """Sign a CommandEnvelope with the Console private key."""
    payload = envelope.model_dump(mode="json")
    return _encode(payload, kp.private_pem(), kid=kid)


def sign_notification(
    kp: PlatformKeypair,
    envelope: NotificationEnvelope,
    kid: str = "platform",
) -> str:
    """Sign a NotificationEnvelope with the Platform private key."""
    payload = envelope.model_dump(mode="json")
    return _encode(payload, kp.private_pem(), kid=kid)


def verify_token(
    token: str,
    public_pem: str,
    *,
    now: int | None = None,
) -> dict[str, Any]:
    """Verify signature + basic envelope claims. Returns the raw payload dict.

    Raises:
        InvalidSignature: bad signature or malformed token.
        ExpiredToken: expires_at claim in the past.
        InvalidPayload: payload missing required envelope fields.
    """
    now = now if now is not None else _now()
    try:
        payload = pyjwt.decode(token, public_pem, algorithms=[ALGORITHM])
    except pyjwt.InvalidSignatureError as exc:
        raise InvalidSignature(str(exc)) from exc
    except pyjwt.DecodeError as exc:
        raise InvalidSignature(str(exc)) from exc

    for required in ("instance_id",):
        if required not in payload:
            raise InvalidPayload(f"missing claim: {required}")

    exp = payload.get("expires_at")
    if exp is not None and int(exp) < now:
        raise ExpiredToken(f"expired at {exp} (now={now})")

    return payload


# Convenience wrapper used by tests that already hold the Ed25519PublicKey.
def verify_with_key(token: str, key: Ed25519PublicKey) -> dict[str, Any]:
    from cryptography.hazmat.primitives import serialization
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return verify_token(token, pem)
