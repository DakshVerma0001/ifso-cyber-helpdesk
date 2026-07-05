from fastapi import APIRouter, Depends

from app.schemas.classifier import ClassifyRequest, ClassifyResponse
from app.services.classifier_service import (
    ClassifierService,
    get_classifier_service,
)

router = APIRouter(
    prefix="/classify",
    tags=["Fraud Classifier"],
)


@router.post(
    "",
    response_model=ClassifyResponse,
    summary="Analyze a suspicious message",
)
async def classify_message(
    request: ClassifyRequest,
    service: ClassifierService = Depends(get_classifier_service),
) -> ClassifyResponse:
    return service.classify(request.message)