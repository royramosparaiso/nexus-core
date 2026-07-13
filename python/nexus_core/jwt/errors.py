"""JWT-related errors."""


class JwtError(Exception):
    """Base error for all JWT operations."""


class ExpiredToken(JwtError):
    pass


class InvalidSignature(JwtError):
    pass


class InvalidPayload(JwtError):
    pass
