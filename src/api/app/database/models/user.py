"""
    User database model.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.database.mixins import TimestampMixin, UUIDMixin
from app.database.models.user_role import UserRole


class User(UUIDMixin, TimestampMixin, Base):
    """
    User database model.
    `User` in this API ecosystem is any authorized human.

    There is UUID as root primary key,
    and `Florgon` (OAuth SSO) user ID as main one SSO system used to sign-in/up to API (user).
    """

    __tablename__ = "users"

    # ID that linked to user by OAuth process (SSO).
    # For now this is `Florgon` one ecosystem SSO via OAuth.
    sso_oauth_user_id = Column(Integer, nullable=False)

    # Information about user.

    # By default, captured from OAuth SSO,
    # if user rejected access, this can reject auth process.
    # (or can be rejected due to not verified email).
    email = Column(String, nullable=False)

    # Permissions.
    # TODO: Review default role.
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False, default=1)
    role: UserRole = relationship(UserRole)
