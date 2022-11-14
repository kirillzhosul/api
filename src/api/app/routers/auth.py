"""
    Auth API router.
    Provides API methods (routes) for working with auth (SSO).
"""

from app.services.api.response import api_error, ApiErrorCode
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/auth/sso")
async def method_auth_sso() -> JSONResponse:
    """Returns token from SSO OAuth code."""

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "SSO auth not implemented yet.")
