from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logger import app_logger
from app.db.init_db import init_database
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import register_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware

from app.api.report import router as report_router
from app.api.evidence import router as evidence_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Initializing database")

    init_database()

    app_logger.info("Database initialized")

    yield

    app_logger.info("Stopping application")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

register_exception_handlers(app)

app.add_middleware(RequestIDMiddleware)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    report_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    evidence_router,
    prefix=settings.API_V1_PREFIX,
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }