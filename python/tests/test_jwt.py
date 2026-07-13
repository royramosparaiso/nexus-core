"""JWT sign/verify round-trip tests."""

import time
from uuid import uuid4

import pytest

from nexus_core.contracts.commands import (
    Command, CommandEnvelope, CommandKind,
)
from nexus_core.jwt import (
    ConsoleKeypair, PlatformKeypair, sign_command, verify_token,
    ExpiredToken, InvalidSignature,
)


def _make_envelope(iid, lifetime=300):
    now = int(time.time())
    return CommandEnvelope(
        instance_id=iid,
        issued_at=now,
        expires_at=now + lifetime,
        command=Command(kind=CommandKind.CREATE_SPACE, payload={"name": "acme"}),
    )


def test_console_sign_and_verify():
    kp = ConsoleKeypair.generate()
    iid = uuid4()
    token = sign_command(kp, _make_envelope(iid))
    payload = verify_token(token, kp.public_pem())
    assert payload["instance_id"] == str(iid)
    assert payload["command"]["kind"] == "create_space"


def test_verify_rejects_wrong_key():
    kp = ConsoleKeypair.generate()
    other = ConsoleKeypair.generate()
    token = sign_command(kp, _make_envelope(uuid4()))
    with pytest.raises(InvalidSignature):
        verify_token(token, other.public_pem())


def test_verify_rejects_expired():
    kp = ConsoleKeypair.generate()
    token = sign_command(kp, _make_envelope(uuid4(), lifetime=-1))
    with pytest.raises(ExpiredToken):
        verify_token(token, kp.public_pem())


def test_platform_and_console_are_symmetric():
    """Same underlying JWT flow, different key roles."""
    console_kp = ConsoleKeypair.generate()
    platform_kp = PlatformKeypair.generate()
    assert console_kp.public_pem() != platform_kp.public_pem()

    # keys can be re-loaded from PEM without losing signing ability
    pem = console_kp.private_pem()
    reloaded = ConsoleKeypair.from_private_pem(pem)
    token = sign_command(reloaded, _make_envelope(uuid4()))
    payload = verify_token(token, console_kp.public_pem())
    assert payload["command"]["kind"] == "create_space"
