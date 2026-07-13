"""Ed25519 keypair management."""

from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)


@dataclass(frozen=True)
class Keypair:
    """Ed25519 keypair. Base class for role-scoped keypairs below."""

    private: Ed25519PrivateKey
    public: Ed25519PublicKey

    @classmethod
    def generate(cls) -> Keypair:
        priv = Ed25519PrivateKey.generate()
        return cls(private=priv, public=priv.public_key())

    def private_pem(self) -> str:
        return self.private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

    def public_pem(self) -> str:
        return self.public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    @classmethod
    def from_private_pem(cls, pem: str) -> Keypair:
        priv = serialization.load_pem_private_key(pem.encode(), password=None)
        if not isinstance(priv, Ed25519PrivateKey):
            raise TypeError("expected Ed25519 private key")
        return cls(private=priv, public=priv.public_key())

    @staticmethod
    def public_from_pem(pem: str) -> Ed25519PublicKey:
        pub = serialization.load_pem_public_key(pem.encode())
        if not isinstance(pub, Ed25519PublicKey):
            raise TypeError("expected Ed25519 public key")
        return pub


class ConsoleKeypair(Keypair):
    """Console-side keypair — signs commands to Platform."""


class PlatformKeypair(Keypair):
    """Platform-side keypair — signs notifications to Console."""
