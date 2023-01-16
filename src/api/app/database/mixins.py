"""
    Mixin classes for the database models.
"""
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class TimestampMixin:
    """
    Adds date-time fields for `created` and `updated`.
    """

    time_created = Column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=False), onupdate=func.now())


class UUIDMixin:
    """
    Adds UUID primary key field.
    """

    # UUID as the primary key.
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False)


__all__ = ["TimestampMixin", "UUIDMixin"]
