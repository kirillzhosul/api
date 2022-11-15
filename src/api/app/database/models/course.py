"""
    Course database model.
"""

# Other
from enum import Enum, auto

# Core model base.
from app.database.core import Base
from sqlalchemy import Boolean, Column, DateTime, Text, Integer, String, ForeignKey

# ORM.
from sqlalchemy.sql import func



class CourseDifficulty(Enum):
    """Difficulty type of the course. """
    easy = auto()
    medium = auto()
    hard = auto()

    trainee = auto()
    junior = auto()
    middle = auto()
    senior = auto()


class Course(Base):
    """Course model. """

    __tablename__ = "courses"

    # Access data.
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(48), nullable=False)

    # Display data.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="...")
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), server_default=func.now())
    difficulty = Column(Integer, nullable=False)
    preview_url = Column(String, nullable=True)

    # Flags.
    is_public = Column(Boolean, nullable=False, default=True) # Means course can be accessed without auth, publicly.
    is_active = Column(Boolean, nullable=False, default=True) # Will never shown in listings.

    # Other.
    price = Column(Integer, default=0, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Times.
    # (database)
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())