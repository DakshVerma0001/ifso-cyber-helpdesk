import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import app_logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.perf_counter()

        response = await call_next(request)

        elapsed = (time.perf_counter() - start) * 1000

        app_logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{elapsed:.2f} ms"
        )

        return response