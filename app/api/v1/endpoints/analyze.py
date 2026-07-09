from fastapi import APIRouter
from fastapi import Depends

from app.api.v1.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
)
from app.services.classification_service import (
    ClassificationService,
    get_classification_service,
)

router = APIRouter(
    prefix="/analyze",
    tags=["AI Analysis"],
)


@router.post(
    "",
    response_model=AnalyzeResponse,
)
def analyze_message(
    request: AnalyzeRequest,
    service: ClassificationService = Depends(
        get_classification_service
    ),
):

    return service.classify(
        request.message
    )