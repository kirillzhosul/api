"""
    Standardized API error codes container.
"""

from enum import Enum


class ApiErrorCode(Enum):
    """API Standardized error codes."""

    API_UNKNOWN_ERROR = 0, 400
    API_INTERNAL_SERVER_ERROR = 1, 500
    API_EXTERNAL_SERVER_ERROR = 2, 500
    API_INVALID_REQUEST = 3, 400
    API_NOT_IMPLEMENTED = 4, 400
    API_METHOD_NOT_FOUND = 5, 404
    API_TOO_MANY_REQUESTS = 6, 429
    API_FORBIDDEN = 7, 403
    API_ITEM_NOT_FOUND = 8, 404
    AUTH_REQUIRED = 10, 401
    AUTH_INVALID_TOKEN = 11, 400
    AUTH_EXPIRED_TOKEN = 12, 400

class ApiErrorException(Exception):
    """
    Exception, that will be return to the user as API error response (FastAPI) handler.
    """

    def __init__(
        self, api_code: ApiErrorCode, message: str = "", data: dict | None = None
    ):
        super().__init__()
        self.api_code = api_code
        self.message = message
        self.data = data
