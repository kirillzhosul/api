"""
    Course CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.course import Course, CourseDifficulty


def get_by_id(db: Session, course_id: int) -> Course:
    """Returns course by it`s ID."""
    return db.query(Course).filter(Course.id == course_id).first()


def get_by_name(db: Session, course_name: str) -> Course:
    """Returns course by it`s name."""
    return db.query(Course).filter(Course.name == course_name).first()


def get_all(db: Session, is_public: bool = True, is_active = True) -> list[Course]:
    """Returns all courses by specified parameters."""
    return db.query(Course).\
        filter(Course.is_public == is_public).\
            filter(Course.is_active == is_active).all()


def create(db: Session, difficulty: CourseDifficulty, owner_id: int, name: str, title: str, description: str = "...", price: int = 0) -> Course:
    """Creates new course."""

    # Create new course.
    course = Course(
        name=name.lower().replace(" ", "-"), 
        difficulty=difficulty.value,
        price=price, 
        owner_id=owner_id, 
        title=title, 
        description=description
    )

    # Apply course in database.
    db.add(course)
    db.commit()
    db.refresh(course)

    return course
