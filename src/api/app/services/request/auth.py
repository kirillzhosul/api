"""
    Request handler and decoder.
    Allows to query auth data from your token or request.
    Root handler for authentication decode.
"""

from typing import Type


from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.database import crud
from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.request.auth_data import AuthData
from app.tokens import AccessToken, BaseToken
from app.config import get_settings, get_logger


def query_auth_data_from_token(
    token: str,
    db: Session,
) -> AuthData:
    """
    Queries authentication data from your token.
    :param token: Token itself.
    :param db: Database session.
    """

    # Decode external token and query auth data from it.
    auth_data = _decode_token(
        token=token,
        token_type=AccessToken,
    )
    return _query_auth_data(
        auth_data=auth_data,
        db=db,
    )


def query_auth_data_from_request(req: Request, db: Session) -> AuthData:
    """
    Queries authentication data from request (from request token).
    :param req: Request itself.
    :param db: Database session.
    """

    # Get token from request and query data from it as external token.
    token = _get_token_from_request(req=req)
    return query_auth_data_from_token(token=token, db=db)


def try_query_auth_data_from_request(
    req: Request,
    db: Session,
) -> tuple[bool, AuthData]:
    """
    Tries query authentication data from request (from request token), and returns tuple with status and auth data.
    :param req: Request itself.
    :param db: Database session.
    """

    try:
        # Try to authenticate, and if does not fall, return OK.
        auth_data = query_auth_data_from_request(req=req, db=db)
        return True, auth_data
    except ApiErrorException:
        # Any exception occurred - unable to authorize.
        return False, None


def _get_token_from_request(req: Request) -> str:
    """
    Returns token from request.
    :param req: Request itself.
    """

    # Simple access token located in header and params.
    # Notice that if user gives header and param, header should taken and param should skiped!
    token_header = req.headers.get("Authorization", "")
    token_param = req.query_params.get("access_token", "")
    return token_header or token_param


def _decode_token(token: str, token_type: Type[BaseToken]) -> AuthData:
    """
    Decodes given token, to payload and session.
    :param token: Token to decode.
    :param token_type: Token type to get.
    :param db: Database session.
    """

    if token_type is not AccessToken:
        raise ValueError("Unexpected type of the token type inside _decode_token!")

    if not token:
        raise ApiErrorException(ApiErrorCode.AUTH_REQUIRED, "Authentication required!")

    # Decode with valid signature.
    settings = get_settings()
    signed_token = token_type.decode(token, key=settings.security_tokens_secret_key)
    if not signed_token.signature_is_valid():
        # If there is invalid signature on the token,
        # means token signed with foreign signature...
        raise ApiErrorException(
            ApiErrorCode.AUTH_INVALID_TOKEN,
            "Unable to validate signature of the token!",
        )

    # Return DTO.
    return AuthData(token=signed_token)


def _query_auth_data(auth_data: AuthData, db: Session) -> AuthData:
    """
    Finalizes query of authentication data by query final user object.
    :param auth_data: Authentication data DTO.
    :param db: Database session.
    """

    # Query database for our user to feed into auth data DTO.
    user_id = auth_data.token.get_subject()
    user = crud.user.get_by_id(db=db, user_id=user_id)

    if not user:
        # Internal authentication system integrity check.
        # users should never be deleted and this should never happen.
        _raise_integrity_check_error()

    # TODO: Check user activity? (is_active)
    # Return modified DTO with user ORM model instance.
    auth_data.user_id = user_id
    auth_data.user = user
    return auth_data


def _raise_integrity_check_error():
    """
    Raises authentication system integrity check error.
    """
    get_logger().warning("Got catched authentication system integrity check failure!")
    raise ApiErrorException(
        ApiErrorCode.AUTH_INVALID_TOKEN,
        "Authentication system integrity check failed!",
    )
