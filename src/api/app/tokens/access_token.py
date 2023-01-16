"""
    API access token implementation.
"""

from .base_token import BaseToken


class AccessToken(BaseToken):
    """
    Access token JWT implementation.
    Used for main authorization, provides access to APIs.
    """

    _type = "access"

    def get_user_id(self) -> str:
        """Returns user ID linked to the token."""
        return self._subject

    def __init__(
        self,
        issuer: str,
        ttl: int | float,
        user_id: str,
        payload: dict | None = None,
        *,
        key: str | None = None
    ):
        super().__init__(issuer, ttl, subject=str(user_id), payload={}, key=key)
