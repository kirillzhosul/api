"""
    Course lecture CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.course_lecture import CourseLecture


def get_by_id(db: Session, course_lecture_id: str) -> CourseLecture:
    """Returns course lecture by it`s ID."""
    return db.query(CourseLecture).filter(CourseLecture.id == course_lecture_id).first()


def get_by_course_id(db: Session, course_id: str) -> CourseLecture:
    """Returns course lectures by it`s course id."""
    return db.query(CourseLecture).filter(CourseLecture.course_id == course_id).all()


def create(
    db: Session, course_id: str, title: str, description="...", content="..."
) -> CourseLecture:
    """Creates new course lecture."""

    # Create new course lecture.
    course_lecture = CourseLecture(
        content=content, title=title, description=description, course_id=course_id
    )

    # Apply course lecture in database.
    db.add(course_lecture)
    db.commit()
    db.refresh(course_lecture)

    return course_lecture
