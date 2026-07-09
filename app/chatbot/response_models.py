from pydantic import BaseModel, Field

from app.chatbot.question_models import Question
from app.services.complaint_models import Complaint

from app.services.evidence_models import EvidenceCollection

class ConversationResponse(BaseModel):

    session_id: str

    completed: bool = False

    question: Question | None = None

    message: str | None = None

    fraud_type: str | None = None

    confidence: float | None = None

    severity: str | None = None

    description: str | None = None

    red_flags: list[str] = Field(default_factory=list)

    recommended_actions: list[str] = Field(default_factory=list)

    evidence_required: list[str] = Field(default_factory=list)

    immediate_actions: list[str] = Field(default_factory=list)

    evidence: EvidenceCollection | None = None

    complaint_ready: bool = False

    complaint: Complaint | None = None