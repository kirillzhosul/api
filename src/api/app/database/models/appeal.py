"""
    Appeal database model.
"""

# Core model base.
from app.database.core import Base
from sqlalchemy import Column, DateTime, Integer, String

# ORM.
from sqlalchemy.sql import func


class Appeal(Base):
    """Appeal model"""

    __tablename__ = "appeals"

    # Access data.
    id = Column(Integer, primary_key=True, index=True)
    contact_email = Column(String, nullable=True)

    # Time.
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())