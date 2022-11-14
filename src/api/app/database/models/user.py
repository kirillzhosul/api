"""
    User database model.
"""

# Core model base.
from app.database.core import Base
from sqlalchemy import Column, DateTime, Integer

# ORM.
from sqlalchemy.sql import func


class User(Base):
    """User model"""

    __tablename__ = "users"

    # Access data.
    id = Column(Integer, primary_key=True, index=True)

    # Time.
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())