from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.logger import logger
import time

"""
    Logging middleware to intercept the requests inside
"""


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"📥 {request.method} {request.url}")

        try:
            response = await call_next(request)
        except Exception as ex:
            logger.exception(f"🔥 Unhandled exception during request: {ex}")
            raise

        process_time = (time.time() - start_time) * 1000
        logger.info(f"📤 {response.status_code} in {process_time:.2f} ms")
        return response
