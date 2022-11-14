"""
    Course lectures API router.
    Provides API methods (routes) for working with course lectures.
"""

from app.services.api.response import api_error, ApiErrorCode
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/courses/lectures/list")
async def method_courses_lectures_list() -> JSONResponse:
    """Returns list of avaliable course lectures."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/get")
async def method_courses_lectures_get() -> JSONResponse:
    """Returns one course lecture by id/name."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/new")
async def method_courses_lectures_new() -> JSONResponse:
    """Creates new course lecture (permitted only)."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/edit")
async def method_courses_lectures_edit() -> JSONResponse:
    """Edits course lecture (permitted only)."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")