"""
    User purchased course database model.
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID

from app.database.core import Base
from app.database.mixins import TimestampMixin, UUIDMixin


class UserCourse(UUIDMixin, TimestampMixin, Base):
    """User purchased course model."""

    __tablename__ = "user_courses"

    # User who is purchased course.
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)

    # Course which was purchased.
    course_id = Column(UUID(as_uuid=False), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="user_courses")

    # Price which user spent at the time when purchasing course.
    purchased_for = Column(Integer, nullable=False)

    @hybrid_property
    def purchased_at(self):
        """
        Returns date-time when course was purchased by user.
        """
        return self.time_created
