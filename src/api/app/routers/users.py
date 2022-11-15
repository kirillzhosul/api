"""
    Users API router.
    Provides API methods (routes) for working with users.
"""

from app.services.api.response import api_error, ApiErrorCode
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/users/me/courses")
async def method_users_me_courses(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns list of your courses."""
    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Users not implemented yet.")


@router.get("/users/list")
async def method_users_list(req: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns list of all users (Permitted only)."""

    query_auth_data_from_request(req, db)
    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "Users not implemented yet.")
