"""
    Course lecture database model serializer.
"""


from app.database.models.course_lecture import CourseLecture
from app.serializers.course import serialize_course

def serialize(
    course_lecture: CourseLecture, show_content: bool = False, 
    serailize_parent_course: bool = False, in_list: bool = False
) -> dict:
    """Returns dict object for API response with serialized course lecture data."""

    serialized_course_lecture = {
        "id": course_lecture.id,
        "course_id": course_lecture.course_id,
        "description": course_lecture.description,
        "is_active": course_lecture.is_active,
        "title": course_lecture.title,
    }

    if serailize_parent_course:
        serialized_user_course |= serialize_course(course_lecture.course, in_list=False)

    if show_content and course_lecture.is_active:
        serialized_course_lecture |= {
            "content": course_lecture.content
        }

    if in_list:
        return serialized_course_lecture

    return {"course_lecture": serialized_course_lecture}


def serialize_list(course_lectures: list[CourseLecture], show_content: bool = False, serailize_parent_course: bool = False) -> dict:
    """Returns dict object for API response with serialized course lectures list data."""

    return {
        "course_lectures": [
            serialize(
                course_lecture=lecture, 
                show_content=show_content, serailize_parent_course=serailize_parent_course, 
                in_list=True
            ) 
            for lecture in course_lectures
        ]
    }


serialize_course_lectures = serialize_list
serialize_course_lecture = serialize