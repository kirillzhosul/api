"""
    Courses API router.
    Provides API methods (routes) for working with courses.
"""

from fastapi import APIRouter, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from app.database import crud
from app.database.dependencies import get_db, Session
from app.database.models.course import CourseDifficulty
from app.config import get_logger
from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import query_auth_data_from_request
from app.serializers.course import serialize_course, serialize_courses
from app.serializers.user_course import serialize_user_course
from app.email.messages import send_purchase_success_email


router = APIRouter()


@router.get("/courses/list")
async def method_courses_list(
    public_only: bool = False,
    active_only: bool = True,
    exclude_foreign_languages: bool = False,
    language: str = "en",
    page: int = 1,
    per_page: int = 5,
    difficulty: str | None = None,
    max_price: int | None = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Returns list of avaliable courses."""

    if 1 > per_page > 10:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST, "`per_page` should between 1 and 10!"
        )
    if page < 1:
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Min `page` is 1!")

    try:
        difficulty_enum = CourseDifficulty[difficulty] if difficulty else None
    except KeyError:
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Invalid difficulty name!")

    courses, courses_total, max_page = crud.course.get_all_filtered_paginated(
        db=db,
        public_only=public_only,
        active_only=active_only,
        language=language if exclude_foreign_languages else None,
        difficulty=difficulty_enum,
        max_price=max_price,
        page=page,
        per_page=per_page,
    )
    current_total = len(courses)
    get_logger().debug(
        f"Listed {current_total} (all: {courses_total}) courses for /courses/list request!"
    )
    return api_success(
        {
            "current_total": current_total,
            "pagination": {
                "total": courses_total,
                "page": page,
                "per_page": per_page,
                "max_page": max_page,
            },
        }
        | serialize_courses(courses)
    )


@router.get("/courses/get")
async def method_courses_get(
    name: str | None = None, course_id: str | None = None, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns one course by id/name."""

    if (not name and not course_id) or (name and course_id):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Please pass `name` or `course_id` (not both)!",
        )

    course = (
        crud.course.get_by_id(db, course_id)
        if course_id
        else crud.course.get_by_name(db, name)
    )
    if not course:
        return api_error(ApiErrorCode.API_ITEM_NOT_FOUND, "Course not found!")
    return api_success(serialize_course(course))


@router.get("/courses/buy")
async def method_courses_buy(
    background_tasks: BackgroundTasks,
    req: Request,
    name: str | None = None,
    course_id: str | None = None,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Buys course by id/name."""
    user = query_auth_data_from_request(req, db).user

    if (not name and not course_id) or (name and course_id):
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST,
            "Please pass `name` or `course_id` (not both)!",
        )

    course = (
        crud.course.get_by_id(db, course_id)
        if course_id
        else crud.course.get_by_name(db, name)
    )
    if not course:
        return api_error(ApiErrorCode.API_ITEM_NOT_FOUND, "Course not found!")
    if course.price > 0:
        if user.role.p_buy_courses_for_free:
            pass
        else:
            return api_error(
                ApiErrorCode.API_FORBIDDEN,
                "Purchasing courses that are not free is not implemented yet!",
            )

    if not user.role.p_buy_courses:
        return api_error(
            ApiErrorCode.API_FORBIDDEN,
            "Your role does not allows to buy courses! Please reach out support!",
        )
    if crud.user_course.get_by_user_id_and_course_id(
        db, user_id=user.id, course_id=course.id
    ):
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "That course is already purchased by you!"
        )

    purchased_course = crud.user_course.create(db, user_id=user.id, course_id=course.id)
    if not purchased_course:
        get_logger().warning(
            "Failed to create new course purchase! "
            f"From user_id: {user.id}, course_id: {course.id}"
        )
        return api_error(
            ApiErrorCode.API_UNKNOWN_ERROR,
            "Failed to purchase course due to unknown error!",
        )

    get_logger().info(
        "New course purchased! "
        f"From user_id: {user.id}, course_id: {course.id}, purchase ID: {purchased_course.id}, price: {course.price}."
    )
    send_purchase_success_email(
        background_tasks, email=user.email, course=course, user_course=purchased_course
    )
    return api_success(serialize_user_course(purchased_course))


@router.get("/courses/new")
async def method_courses_new(
    req: Request,
    difficulty: str,
    name: str,
    title: str,
    description: str,
    price: int = 0,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Creates new course (permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_create_courses:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    try:
        difficulty_enum = CourseDifficulty[difficulty]
    except KeyError:
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Invalid difficulty name!")

    course = crud.course.create(
        db,
        difficulty=difficulty_enum,
        owner_id=user.id,
        name=name,
        price=price,
        title=title,
        description=description,
    )
    if not course:
        get_logger().warning(f"Failed to create course object due to unexpected error!")
        return api_error(ApiErrorCode.API_UNKNOWN_ERROR, "Failed to create new course!")
    return api_success(serialize_course(course))


@router.get("/courses/edit")
async def method_courses_edit(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Edits course (permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_edit_courses:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    return api_error(
        ApiErrorCode.API_NOT_IMPLEMENTED,
        "Editing of the courses is not implemented yet!",
    )
