"""
    User purchased course database model serializer.
"""

import time

from app.database.models.user_course import UserCourse
from app.serializers.course import serialize_course

def serialize(user_course: UserCourse, serailize_parent_course: bool = True,in_list: bool = False) -> dict:
    """Returns dict object for API response with serialized user purchased course data."""

    serialized_user_course = {
        "purchase_id": user_course.id,
        "course_id": user_course.course_id,
        "purchased_for": user_course.purchased_for,
        "purchased_at": time.mktime(user_course.time_purchased.timetuple()),
    }
    
    if serailize_parent_course:
        serialized_user_course |= serialize_course(user_course.course, in_list=False)

    if in_list:
        return serialized_user_course

    return {"purchased_course": serialized_user_course}


def serialize_list(user_courses: list[UserCourse]) -> dict:
    """Returns dict object for API response with serialized user purchased courses list data."""

    return {
        "purchased_courses": [
            serialize(user_course=user_course, serailize_parent_course=True, in_list=True) 
            for user_course in user_courses
        ]
    }


serialize_user_courses = serialize_list
serialize_user_course = serialize