"""
    API exception handlers.
    (FastAPI exception handlers)
"""

from app.services.api.errors import ApiErrorCode, ApiErrorException
from app.services.api.response import api_error


async def validation_exception_handler(_, exception):
    """Custom validation exception handler."""
    return api_error(
        ApiErrorCode.API_INVALID_REQUEST, "Invalid request!", {"exc": str(exception)}
    )


async def too_many_requests_handler(_, exception):
    """Limiter too many requests exception handler."""
    return api_error(
        ApiErrorCode.API_TOO_MANY_REQUESTS,
        "Too Many Requests! You are sending requests too fast. Please try again later.",
        {"retry-after": int(exception.headers["Retry-After"])},
        headers=exception.headers,
    )


async def api_error_exception_handler(_, e: ApiErrorException):
    """Handler for FastAPI pydantic exceptions."""
    return api_error(e.api_code, e.message, e.data)


async def not_found_handler(_, __):
    """Handler for FastAPI not found router error."""
    return api_error(
        ApiErrorCode.API_METHOD_NOT_FOUND,
        "Method not found! Please read documentation.",
    )


async def internal_server_error_handler(_, __):
    """Handler for FastAPI internal server error."""
    return api_error(
        ApiErrorCode.API_INTERNAL_SERVER_ERROR,
        "Internal server error! Server is unavailable at this time. Please try again later.",
    )
