"""
    Courses API router.
    Provides API methods (routes) for working with courses.
"""

from app.services.api.response import api_error, ApiErrorCode
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/courses/list")
async def method_courses_list(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns list of avaliable courses."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/get")
async def method_courses_get(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns one course by id/name."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/new")
async def method_courses_new(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Creates new course (permitted only)."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")


@router.get("/courses/edit")
async def method_courses_edit(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Edits course (permitted only)."""
    
    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Courses not implemented yet.")