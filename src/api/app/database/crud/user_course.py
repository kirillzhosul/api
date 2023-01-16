"""
    User purchased course CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.user_course import UserCourse
from app.database import crud


def get_by_id(db: Session, user_course_id: str) -> UserCourse:
    """Returns user course by it`s ID."""
    return db.query(UserCourse).filter(UserCourse.id == user_course_id).first()


def get_by_user_id(db: Session, user_id: str) -> UserCourse:
    """Returns user courses by owner user ID."""
    return db.query(UserCourse).filter(UserCourse.user_id == user_id).all()


def get_by_user_id_and_course_id(
    db: Session, user_id: str, course_id: str
) -> UserCourse:
    """Returns user course by owner user ID and course."""
    return (
        db.query(UserCourse)
        .filter(UserCourse.user_id == user_id)
        .filter(UserCourse.course_id == course_id)
        .all()
    )


def create(db: Session, user_id: str, course_id: str) -> UserCourse:
    """Creates new user purchased course."""

    # Create new user purchased course.
    course = crud.course.get_by_id(db, course_id)
    user_course = UserCourse(
        user_id=user_id, course_id=course_id, purchased_for=course.price
    )

    # Apply user course in database.
    db.add(user_course)
    db.commit()
    db.refresh(user_course)

    return user_course
