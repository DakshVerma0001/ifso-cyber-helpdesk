from fastapi import APIRouter, Depends, HTTPException

from app.schemas.chat import (
    ChatReplyRequest,
    ChatReplyResponse,
    StartConversationResponse,
)
from app.services.chatbot_service import (
    ChatbotService,
    get_chatbot_service,
)

router = APIRouter(
    prefix="/chat",
    tags=["AI Cyber Investigation Assistant"],
)


@router.post(
    "/start",
    response_model=StartConversationResponse,
    summary="Start a new cyber fraud investigation session",
)
async def start_conversation(
    service: ChatbotService = Depends(get_chatbot_service),
):
    response = service.start()

    return StartConversationResponse(**response.model_dump())


@router.post(
    "/reply",
    response_model=ChatReplyResponse,
    summary="Submit an answer and receive the next investigation step",
)
async def reply(
    request: ChatReplyRequest,
    service: ChatbotService = Depends(get_chatbot_service),
):
    try:

        response = service.reply(
            session_id=request.session_id,
            answer=request.answer,
        )

        return ChatReplyResponse(**response.model_dump())

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )