"""
    Course database model.
"""

from enum import Enum, auto

from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, Text, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.core import Base
from app.database.mixins import UUIDMixin, TimestampMixin


class CourseDifficulty(Enum):
    """Difficulty type of the course."""

    easy = auto()
    medium = auto()
    hard = auto()

    trainee = auto()
    junior = auto()
    middle = auto()
    senior = auto()


class Course(UUIDMixin, TimestampMixin, Base):
    """Course model."""

    __tablename__ = "courses"

    # Access data.
    name = Column(String(48), nullable=False, unique=True)

    # Display data.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="...")
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), server_default=func.now())
    difficulty = Column(Integer, nullable=False)
    preview_url = Column(String, nullable=True)

    # Flags.
    is_public = Column(
        Boolean, nullable=False, default=True
    )  # Means course can be accessed without auth, publicly.
    is_active = Column(
        Boolean, nullable=False, default=True
    )  # Will never shown in listings.

    # Other.
    price = Column(Integer, default=0, nullable=False)
    owner_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    user_courses = relationship("UserCourse", back_populates="course")
    course_lectures = relationship("CourseLecture", back_populates="course")
