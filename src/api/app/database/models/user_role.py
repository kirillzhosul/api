"""
    User role database model.
"""

from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql import expression

from app.database.core import Base
from app.database.mixins import TimestampMixin


class UserRole(TimestampMixin, Base):
    """
    User role model.
    Implementes user role system when users has role that is managed permissions granted to that role.
    """

    __tablename__ = "user_roles"

    # Access data.
    # (Not UUID as it is not required there)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)

    # Permissions && settings.

    # Users.
    p_list_users = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    p_manage_users = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )

    # Roles.
    p_manage_roles = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )

    # Courses.
    # (Including lectures).
    p_buy_courses = Column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )
    p_buy_courses_for_free = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    p_create_courses = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    p_edit_courses = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )

    # Mailings.
    p_manage_mailings = Column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
