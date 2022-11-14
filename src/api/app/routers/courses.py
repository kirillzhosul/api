"""
    Courses API router.
    Provides API methods (routes) for working with courses.
"""

from app.services.api.response import api_error, ApiErrorCode
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/courses/list")
async def method_courses_list() -> JSONResponse:
    """Returns list of avaliable courses."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/get")
async def method_courses_get() -> JSONResponse:
    """Returns one course by id/name."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/new")
async def method_courses_new() -> JSONResponse:
    """Creates new course (permitted only)."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/edit")
async def method_courses_edit() -> JSONResponse:
    """Edits course (permitted only)."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")