from pydantic import BaseModel, Field

from app.chatbot.question_models import Question


class ConversationResponse(BaseModel):
    session_id: str

    completed: bool = False

    question: Question | None = None

    message: str | None = None

    fraud_type: str | None = None

    immediate_actions: list[str] = Field(default_factory=list)

    complaint_ready: bool = False