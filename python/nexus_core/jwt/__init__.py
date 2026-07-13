"""Ed25519 JWT signing/verification for the Nexus protocol."""

from nexus_core.jwt.keys import ConsoleKeypair, PlatformKeypair, Keypair
from nexus_core.jwt.sign import sign_command, sign_notification, verify_token
from nexus_core.jwt.errors import JwtError, ExpiredToken, InvalidSignature

__all__ = [
    "ConsoleKeypair", "PlatformKeypair", "Keypair",
    "sign_command", "sign_notification", "verify_token",
    "JwtError", "ExpiredToken", "InvalidSignature",
]
