"""
    Course lectures API router.
    Provides API methods (routes) for working with course lectures.
"""

from app.services.api.response import api_error, api_success, ApiErrorCode
from app.services.request.auth import (
    query_auth_data_from_request,
    try_query_auth_data_from_request,
)
from app.database.dependencies import get_db, Session
from app.database import crud
from app.config import get_logger
from app.database.models.course import Course
from app.serializers.course_lecture import (
    serialize_course_lecture,
    serialize_course_lectures,
)
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


def user_has_access_to_course_content(
    db: Session, user_id: str | None, course: Course
) -> bool:
    """
    Returns true if user has access to that course
    :param user_id: If none, means unauthorized user.
    """
    if not course.is_public:
        if user_id is None:
            return False
        user_course = crud.user_course.get_by_user_id_and_course_id(
            db=db, user_id=user_id, course_id=course.id
        )
        return user_course is not None
    return True


@router.get("/courses/lectures/list")
async def method_courses_lectures_list(
    req: Request,
    course_id: str | None = None,
    course_name: str | None = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Returns list of avaliable course lectures."""

    if (not course_name and not course_id) or (course_name and course_id):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Please pass `course_name` or `course_id` (not both)!",
        )

    is_authenticated, auth_data = try_query_auth_data_from_request(req, db)
    user_id = auth_data.user_id if is_authenticated else None

    course = (
        crud.course.get_by_id(db, course_id)
        if course_id
        else crud.course.get_by_name(db, course_name)
    )
    if not course:
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Course with that ID or name not found!"
        )

    user_has_access_to_content = user_has_access_to_course_content(db, user_id, course)
    return api_success(
        serialize_course_lectures(
            course_lectures=crud.course_lecture.get_by_course_id(
                db, course_id=course_id
            ),
            show_content=user_has_access_to_content,
        )
        | {"content_hidden_until_purchase": not user_has_access_to_content}
    )


@router.get("/courses/lectures/get")
async def method_courses_lectures_get(
    req: Request,
    course_lecture_id: str,
    course_id: str | None = None,
    course_name: str | None = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Returns one course lecture by id/name."""

    if (not course_name and not course_id) or (course_name and course_id):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Please pass `course_name` or `course_id` (not both)!",
        )

    is_authenticated, auth_data = try_query_auth_data_from_request(req, db)
    user_id = auth_data.user_id if is_authenticated else None

    course = (
        crud.course.get_by_id(db, course_id)
        if course_id
        else crud.course.get_by_name(db, course_name)
    )
    if not course:
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Course with that ID or name not found!"
        )

    course_lecture = crud.course_lecture.get_by_id(
        db, course_lecture_id=course_lecture_id
    )
    if not course_lecture:
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Course lecture with that ID not found!"
        )
    if course_lecture.course_id != course.id:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "That course lecture does not belongs to requested course!",
        )

    user_has_access_to_content = user_has_access_to_course_content(db, user_id, course)
    return api_success(
        serialize_course_lecture(
            course_lecture=course_lecture, show_content=user_has_access_to_content
        )
        | {"content_hidden_until_purchase": not user_has_access_to_content}
    )


@router.get("/courses/lectures/new")
async def method_courses_lectures_new(
    req: Request,
    course_id: int,
    title: str,
    description: str = "...",
    content: str = "...",
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Creates new course lecture (permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_create_courses:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    course = crud.course.get_by_id(db, course_id=course_id)
    if not course:
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Course with that ID not found!"
        )

    course_lecture = crud.course_lecture.create(
        db=db,
        course_id=course.id,
        title=title,
        description=description,
        content=content,
    )
    if not course_lecture:
        get_logger().warning(
            f"Failed to create course lecture object due to unexpected error!"
        )
        return api_error(
            ApiErrorCode.API_UNKNOWN_ERROR, "Failed to create new course lecture!"
        )
    return api_success(serialize_course_lecture(course_lecture, show_content=True))


@router.get("/courses/lectures/edit")
async def method_courses_lectures_edit(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Edits course lecture (permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_edit_courses:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")
