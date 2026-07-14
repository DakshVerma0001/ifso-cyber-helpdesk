from fastapi import APIRouter

from pydantic import BaseModel

from app.services.awareness_service import (
    AwarenessService,
)


router = APIRouter(
    prefix="/awareness",
    tags=["Cyber Fraud Awareness"],
)


class AwarenessRequest(BaseModel):

    message: str


@router.post("/chat")
def awareness_chat(
    request: AwarenessRequest,
):

    response = AwarenessService().answer(
        request.message
    )

    return response