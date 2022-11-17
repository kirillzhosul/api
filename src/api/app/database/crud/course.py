"""
    Course CRUD utils for the database.
"""

from math import ceil
from sqlalchemy.orm import Session
from app.database.models.course import Course, CourseDifficulty


def get_by_id(db: Session, course_id: int) -> Course:
    """Returns course by it`s ID."""
    return db.query(Course).filter(Course.id == course_id).first()


def get_by_name(db: Session, course_name: str) -> Course:
    """Returns course by it`s name."""
    return db.query(Course).filter(Course.name == course_name).first()


def get_all_filtered_paginated(db: Session, 
    public_only: bool = True, active_only: bool = True, 
    language: str | None = None,
    per_page: int = 5, page: int = 1
) -> tuple[list[Course], int, int]:
    """Returns all courses by specified parameters."""
    query = db.query(Course)
    if active_only:
        query = query.filter(Course.is_active == active_only)
    if public_only:
        query = query.filter(Course.is_public == public_only)
    if language:
        pass

    max_page = ceil(courses_total / per_page)
    page_offset = per_page * (page - 1)
    
    courses_total = query.count()
    query = query.\
        offset(offset=page_offset).\
            limit(limit=per_page)
    courses = query.all()
    return courses, courses_total, max_page


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
