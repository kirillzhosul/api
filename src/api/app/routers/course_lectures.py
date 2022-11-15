"""
    Course lectures API router.
    Provides API methods (routes) for working with course lectures.
"""

from app.services.api.response import api_error, ApiErrorCode
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/courses/lectures/list")
async def method_courses_lectures_list(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns list of avaliable course lectures."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/get")
async def method_courses_lectures_get(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns one course lecture by id/name."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/new")
async def method_courses_lectures_new(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Creates new course lecture (permitted only)."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/lectures/edit")
async def method_courses_lectures_edit(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Edits course lecture (permitted only)."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")