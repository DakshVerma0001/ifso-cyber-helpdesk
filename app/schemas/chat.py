from pydantic import BaseModel, Field

from app.services.complaint_models import Complaint


class StartConversationResponse(BaseModel):

    session_id: str

    completed: bool

    question: dict

    message: str | None = None

    fraud_type: str | None = None

    confidence: float | None = None

    severity: str | None = None

    description: str | None = None

    red_flags: list[str] = Field(default_factory=list)

    recommended_actions: list[str] = Field(default_factory=list)

    evidence_required: list[str] = Field(default_factory=list)

    immediate_actions: list[str] = Field(default_factory=list)

    complaint_ready: bool = False

    complaint: Complaint | None = None


class ChatReplyRequest(BaseModel):

    session_id: str = Field(..., min_length=1)

    answer: str = Field(..., min_length=1)


class ChatReplyResponse(BaseModel):

    session_id: str

    completed: bool

    question: dict | None = None

    message: str | None = None

    fraud_type: str | None = None

    confidence: float | None = None

    severity: str | None = None

    description: str | None = None

    red_flags: list[str] = Field(default_factory=list)

    recommended_actions: list[str] = Field(default_factory=list)

    evidence_required: list[str] = Field(default_factory=list)

    immediate_actions: list[str] = Field(default_factory=list)

    complaint_ready: bool = False

    complaint: Complaint | None = None