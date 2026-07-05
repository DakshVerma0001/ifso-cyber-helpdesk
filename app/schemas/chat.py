from pydantic import BaseModel, Field


class StartConversationResponse(BaseModel):
    session_id: str
    completed: bool
    question: dict
    message: str | None = None
    fraud_type: str | None = None
    immediate_actions: list[str] = Field(default_factory=list)
    complaint_ready: bool = False


class ChatReplyRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class ChatReplyResponse(BaseModel):
    session_id: str
    completed: bool
    question: dict | None = None
    message: str | None = None
    fraud_type: str | None = None
    immediate_actions: list[str] = Field(default_factory=list)
    complaint_ready: bool = False