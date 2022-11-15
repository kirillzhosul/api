"""
    Course CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.course import Course


def get_by_id(db: Session, course_id: int) -> Course:
    """Returns course by it`s ID."""
    return db.query(Course).filter(Course.id == course_id).first()
