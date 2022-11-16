"""
    Courses API router.
    Provides API methods (routes) for working with courses.
"""

from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from app.database.models.course import CourseDifficulty
from app.serializers.course import serialize_course, serialize_courses
from app.serializers.user_course import serialize_user_course
from app.database import crud
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/courses/list")
async def method_courses_list(public_only: bool = False, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns list of avaliable courses."""

    courses = crud.course.get_public(db) if public_only else crud.course.get_active(db)
    return api_success({
        "total": len(courses)
    } | serialize_courses(courses))


@router.get("/courses/get")
async def method_courses_get(name: str | None = None, course_id: int | None = None, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns one course by id/name."""

    if (not name and not course_id) or (name and course_id):
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Please pass `name` or `course_id` (not both)!")

    course = crud.course.get_by_id(db, course_id) if course_id else crud.course.get_by_name(db, name)
    if not course:
        return api_error(ApiErrorCode.API_ITEM_NOT_FOUND, "Course not found!")
    return api_success(serialize_course(course))


@router.get("/courses/buy")
async def method_courses_buy(req: Request, name: str | None = None, course_id: int | None = None, db: Session = Depends(get_db)) -> JSONResponse:
    """Buys course by id/name."""
    user_id = query_auth_data_from_request(req, db).user.id

    if (not name and not course_id) or (name and course_id):
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Please pass `name` or `course_id` (not both)!")

    course = crud.course.get_by_id(db, course_id) if course_id else crud.course.get_by_name(db, name)
    if not course:
        return api_error(ApiErrorCode.API_ITEM_NOT_FOUND, "Course not found!")
    if course.price > 0:
        return api_error(ApiErrorCode.API_FORBIDDEN, "Purchasing courses that are not free is not implemented yet!")

    if crud.user_course.get_by_user_id_and_course_id(db, user_id=user_id, course_id=course.id):
        return api_error(ApiErrorCode.API_FORBIDDEN, "That course is already purchased by you!")

    purchased_course = crud.user_course.create(db, user_id=user_id, course_id=course.id)    
    return api_success(serialize_user_course(purchased_course))


@router.get("/courses/new")
async def method_courses_new(req: Request, difficulty: str, name: str, title: str, description: str, price: int = 0, db: Session = Depends(get_db)) -> JSONResponse:
    """Creates new course (permitted only)."""

    auth_data = query_auth_data_from_request(req, db)
    if not auth_data.user.is_admin:
        return api_error(ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!")
    
    try:
        difficulty_enum = CourseDifficulty[difficulty]
    except KeyError:
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Invalid difficulty name!")

    course = crud.course.create(db, 
        difficulty=difficulty_enum, 
        owner_id=auth_data.user_id, 
        name=name, 
        price=price, 
        title=title, description=description
    )
    if not course:
        return api_error(ApiErrorCode.API_UNKNOWN_ERROR, "Failed to create new course!")
    return api_success(serialize_course(course))


@router.get("/courses/edit")
async def method_courses_edit(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Edits course (permitted only)."""
    
    auth_data = query_auth_data_from_request(req, db)
    if not auth_data.user.is_admin:
        return api_error(ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!")
    
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Editing of the courses is not implemented yet!")