"""
    Gatey logging middleware.
"""

from starlette.types import ASGIApp, Receive, Scope, Send
from app.config import get_gatey_client, get_logger


class GateyMiddleware:
    """Gatey (error) logging middleware."""

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            gatey_client = get_gatey_client()
            if gatey_client:
                get_logger().debug("Got captured Gatey exception! Sending to Gatey client...")
                get_gatey_client().capture_exception(e)
            raise e
        return