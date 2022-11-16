"""
    User purchased course database model.
"""

# Core model base.
from app.database.core import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Integer, ForeignKey

# ORM.
from sqlalchemy.sql import func


class UserCourse(Base):
    """User purchased course model. """

    __tablename__ = "user_courses"

    # Access data.
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    course_id = Column(ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="user_courses")

    # Price.
    purchased_for = Column(Integer, nullable=False)

    # Times.
    time_purchased = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )