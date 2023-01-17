"""
    DTO for authentication request.
"""

from app.database.models.user import User
from app.tokens import BaseToken


class AuthData:
    """DTO for authenticated request."""

    user: User
    token: BaseToken

    def __init__(
        self,
        token: BaseToken,
        user_id: str | None = None,
        user: User | None = None,
    ) -> None:
        """
        :param token: Session or access token object.
        :param user_id: SSO user ID (and native, because they are same).
        :param user: User database model object.
        """
        self.user_id = user_id
        self.user = user
        self.token = token
