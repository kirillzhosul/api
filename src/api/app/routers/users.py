"""
    Users API router.
    Provides API methods (routes) for working with users.
"""

from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from app.serializers.user import serialize_user, serialize_users
from app.serializers.user_course import serialize_user_courses
from app.database import crud
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/users/me")
async def method_users_me(
    req: Request, show_courses: bool = False, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns id, email for current user."""
    auth_data = query_auth_data_from_request(req, db)

    serialized_user = serialize_user(auth_data.user)
    if show_courses:
        purchased_courses = crud.user_course.get_by_user_id(
            db, user_id=auth_data.user_id
        )
        return api_success(serialized_user | serialize_user_courses(purchased_courses))
    return api_success(serialized_user)


@router.get("/users/me/courses")
async def method_users_me_courses(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns list of your courses."""
    auth_data = query_auth_data_from_request(req, db)

    purchased_courses = crud.user_course.get_by_user_id(db, user_id=auth_data.user_id)
    return api_success(
        {"total": len(purchased_courses)} | serialize_user_courses(purchased_courses)
    )


@router.get("/users/list")
async def method_users_list(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns list of all users (Permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_list_users:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    users = crud.user.get_all(db)
    return api_success({"total": len(users)} | serialize_users(users))
