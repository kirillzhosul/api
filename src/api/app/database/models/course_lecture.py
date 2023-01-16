"""
    Course lecture database model.
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Text, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.core import Base
from app.database.mixins import UUIDMixin, TimestampMixin


class CourseLecture(UUIDMixin, TimestampMixin, Base):
    """Course model."""

    __tablename__ = "course_lectures"

    # Access data.
    course_id = Column(UUID(as_uuid=False), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="course_lectures")

    # Display data.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="...")

    # Content.
    content = Column(Text, nullable=False, default="...")

    # Flags.
    is_active = Column(
        Boolean, nullable=False, default=True
    )  # Will shown as closed (unfinished).
