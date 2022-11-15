"""
    Auth API router.
    Provides API methods (routes) for working with auth (SSO).
"""

import requests

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.config import get_settings, Settings, get_logger
from app.database import crud
from app.database.dependencies import get_db, Session
from app.services.api.response import ApiErrorCode, api_error, api_success
from app.tokens.access_token import AccessToken

router = APIRouter()


def send_sso_oauth_exchange_request(oauth_code: str, settings: Settings, timeout: int = 5):
    """
        Sends OAuth exchange request to SSO server and returns response.
    """
    exchange_method = f"{settings.sso_api_url}/{settings.sso_api_oauth_exchange}"
    exchange_client_params = f"client_secret={settings.sso_api_client_secret}&client_id={settings.sso_api_client_id}&redirect_uri={settings.sso_api_redirect_uri}"
    exchange_params = f"{exchange_client_params}&code={oauth_code}&grant_type=authorization_code"
    exchange_response = requests.get(f"{exchange_method}?{exchange_params}", timeout=timeout)
    return exchange_response


@router.get("/auth/sso")
async def method_auth_sso(code: str, db: Session = Depends(get_db)) -> JSONResponse:
    """Returns token from SSO OAuth code."""

    settings = get_settings()
    logger = get_logger()

    exchange_response = send_sso_oauth_exchange_request(oauth_code=code, settings=settings)
    exchange_json = exchange_response.json()
    exchange_error, exchange_data = \
        exchange_json.get("error"), exchange_json.get("success")

    if exchange_error:
        logger.warning(f"Failed to authenticate user with SSO! External server returned error code: '{exchange_error.get('code')}', with message: '{exchange_error.get('message')}'")
        return api_error(ApiErrorCode.API_UNKNOWN_ERROR, "SSO failed to exchange auth process and verify your auth.", {
            "sso_error": exchange_error
        })
    
    sso_user_email = exchange_data.get("email")
    sso_user_id = exchange_data.get("user_id")
    if not sso_user_email or not sso_user_id:
        return api_error(ApiErrorCode.API_FORBIDDEN, "Unable to query required data from exchanged request. Please review granted OAuth permissions!")
    
    current_user = crud.user.get_or_create(db, user_id=sso_user_id, email=sso_user_email)
    access_token_ttl = settings.security_access_tokens_ttl
    access_token = AccessToken(
        issuer=settings.security_tokens_issuer, 
        ttl=access_token_ttl, 
        user_id=current_user.id, 
    ).encode(key=settings.security_tokens_secret_key)

    logger.info(f"Successfully authorized UID-{current_user.id}!")
    return api_success({
        "access_token": access_token,
        "user_id": current_user.id,
        "expires_in": access_token_ttl,
    })
