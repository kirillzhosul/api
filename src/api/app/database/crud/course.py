"""
    Course CRUD utils for the database.
"""

from math import ceil
from sqlalchemy.orm import Session
from app.database.models.course import Course, CourseDifficulty


def get_by_id(db: Session, course_id: str) -> Course:
    """Returns course by it`s ID."""
    return db.query(Course).filter(Course.id == course_id).first()


def get_by_name(db: Session, course_name: str) -> Course:
    """Returns course by it`s name."""
    return db.query(Course).filter(Course.name == course_name).first()


def get_all_filtered_paginated(
    db: Session,
    public_only: bool = True,
    active_only: bool = True,
    language: str | None = None,
    max_price: int | None = None,
    difficulty: CourseDifficulty | None = None,
    per_page: int = 5,
    page: int = 1,
) -> tuple[list[Course], int, int]:
    """Returns all courses by specified parameters."""
    if per_page < 1 or page < 1:
        raise ValueError("per_page and page should be >= 1")

    query = db.query(Course)
    if active_only:
        query = query.filter(Course.is_active == active_only)
    if public_only:
        query = query.filter(Course.is_public == public_only)
    if max_price:
        query = query.filter(Course.price <= max_price)
    if difficulty:
        query = query.filter(Course.difficulty == difficulty.value)
    if language:
        pass

    # Total courses in database for that query (without pagination).
    courses_total = query.count()

    # Calculate values.
    max_page = ceil(courses_total / per_page)
    page_offset = per_page * (page - 1)

    # Paginate and return query courses.
    query = query.offset(offset=page_offset).limit(limit=per_page)
    courses = query.all()

    return courses, courses_total, max_page


def create(
    db: Session,
    difficulty: CourseDifficulty,
    owner_id: str,
    name: str,
    title: str,
    description: str = "...",
    price: int = 0,
) -> Course:
    """Creates new course."""

    # Create new course.
    course = Course(
        name=name.lower().replace(" ", "-"),
        difficulty=difficulty.value,
        price=price,
        owner_id=owner_id,
        title=title,
        description=description,
    )

    # Apply course in database.
    db.add(course)
    db.commit()
    db.refresh(course)

    return course
