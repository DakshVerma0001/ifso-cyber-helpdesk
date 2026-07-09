from fastapi import APIRouter

from app.api.v1.endpoints.classifier import router as classifier_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.analyze import (
    router as analyze_router,
)   

api_router = APIRouter()

api_router.include_router(health_router)

api_router.include_router(classifier_router)

api_router.include_router(chat_router)

api_router.include_router(
    analyze_router
)