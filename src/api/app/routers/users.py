"""
    Users API router.
    Provides API methods (routes) for working with users.
"""

from app.services.api.response import api_error, ApiErrorCode
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/users/me/courses")
async def method_users_me_courses() -> JSONResponse:
    """Returns list of your courses."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Users not implemented yet.")


@router.get("/users/list")
async def method_users_list() -> JSONResponse:
    """Returns list of all users (Permitted only)."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Users not implemented yet.")
