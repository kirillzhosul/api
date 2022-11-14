"""
    Course lecture database model.
"""

# Core model base.
from app.database.core import Base
from sqlalchemy import Boolean, Column, DateTime, Text, Integer, String, ForeignKey

# ORM.
from sqlalchemy.sql import func

class CourseLecture(Base):
    """Course model. """

    __tablename__ = "course_lectures"

    # Access data.
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    course_id = Column(ForeignKey("courses.id"), nullable=False)

    # Display data.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="...")

    # Content.
    content = Column(Text, nullable=False, default="...")

    # Flags.
    is_active = Column(Boolean, nullable=False, default=True) # Will shown as closed (unfinished).

    # Times.
    # (database)
    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())