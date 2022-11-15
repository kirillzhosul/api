"""
    Course database model serializer.
"""

import time

from app.database.dependencies import Session
from app.database.models.course import Course, CourseDifficulty

def serialize(db: Session, course: Course, in_list: bool = False):
    """Returns dict object for API response with serialized course data."""

    serialized_course = {
        "id": course.id,
        "name": course.name,
        "title": course.title,
        "description": course.description,
        "preview_url": course.preview_url if course.preview_url else None,
        "is_public": course.is_public,
        "is_active": course.is_active,
        "price": course.price,
        "difficulty": {
            "name": CourseDifficulty(course.difficulty).name,
            "value": CourseDifficulty(course.difficulty).name,
        },
        "published_at": time.mktime(course.published_at.timetuple()),
        "edited_at": time.mktime(course.edited_at.timetuple()),
    }


    if in_list:
        return serialized_course

    return {"course": serialized_course}


def serialize_list(db: Session, courses: list[Course]) -> dict:
    """Returns dict object for API response with serialized courses list data."""

    return {
        "courses": [serialize(db=db, course=course, in_list=True) for course in courses]
    }


serialize_courses = serialize_list
serialize_course = serialize