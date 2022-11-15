"""
    User purchased course database model serializer.
"""

import time

from app.database.dependencies import Session
from app.database.models.user_course import UserCourse

def serialize(db: Session, user_course: UserCourse, in_list: bool = False):
    """Returns dict object for API response with serialized user purchased course data."""

    serialized_user_course = {
        "id": user_course.id,
        "purchased_for": user_course.purchased_for,
        "purchased_at": time.mktime(user_course.time_purchased.timetuple()),
    }

    if in_list:
        return serialized_user_course

    return {"purchased_course": serialized_user_course}


def serialize_list(db: Session, user_courses: list[UserCourse]) -> dict:
    """Returns dict object for API response with serialized user purchased courses list data."""

    return {
        "purchased_courses": [serialize(db=db, user_course=user_course, in_list=True) for user_course in user_courses]
    }


serialize_user_courses = serialize_list
serialize_user_course = serialize