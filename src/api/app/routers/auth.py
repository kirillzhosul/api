"""
    Auth API router.
    Provides API methods (routes) for working with auth (SSO).
"""

from app.config import get_settings
from app.services.api.response import api_error, ApiErrorCode
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests

router = APIRouter()


@router.get("/auth/sso")
async def method_auth_sso(code: str) -> JSONResponse:
    """Returns token from SSO OAuth code."""

    settings = get_settings()

    exchange_timeout = 5
    exchange_method = f"{settings.sso_api_url}/{settings.sso_api_oauth_exchange}"
    exchange_params = f"code={code}&client_secret={settings.sso_api_client_secret}&client_id={settings.sso_api_client_id}&redirect_uri={settings.sso_api_redirect_uri}"
    exchange_req = requests.get(f"{exchange_method}?{exchange_params}", timeout=exchange_timeout)

    exchange_json = exchange_req.json()

    if exchange_json.get("error"):
        return api_error(ApiErrorCode.API_UNKNOWN_ERROR, "SSO failed to exchange auth process and verify your auth.", {
            "additional_info": exchange_json
        })

    return api_error(ApiErrorCode.API_NOT_IMPLEMENTED, "SSO auth not implemented yet.", {
        "additional_info": exchange_json
    })
