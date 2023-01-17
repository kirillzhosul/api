"""
    API routers.
    (FastAPI routers)
"""

from app.config import get_settings
from fastapi import FastAPI

from . import utils, auth, courses, course_lectures, users, mailing, roles


def include_routers(app: FastAPI) -> None:
    """
    Registers (Including) FastAPI routers for FastAPI app.
    """
    settings = get_settings()
    proxy_url_prefix = settings.proxy_url_prefix
    for module in [utils, auth, courses, course_lectures, users, mailing, roles]:
        app.include_router(module.router, prefix=proxy_url_prefix)
