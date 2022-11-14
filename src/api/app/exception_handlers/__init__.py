"""
    API exception handlers.
    (FastAPI exception handlers)
"""

from app.services.api.errors import ApiErrorException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from . import _handlers


def add_exception_handlers(app: FastAPI) -> None:
    """
    Adds exception handlers for application.
    """

    app.add_exception_handler(ApiErrorException, _handlers.api_error_exception_handler)
    app.add_exception_handler(
        RequestValidationError, _handlers.validation_exception_handler
    )

    app.add_exception_handler(429, _handlers.too_many_requests_handler)

    app.add_exception_handler(404, _handlers.not_found_handler)
    app.add_exception_handler(500, _handlers.internal_server_error_handler)
