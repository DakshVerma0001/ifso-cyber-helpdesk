from datetime import datetime
from pydantic import BaseModel, Field


class ConversationSession(BaseModel):
    session_id: str

    current_state: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    intent: str | None = None

    fraud_type: str | None = None

    money_lost: bool | None = None

    amount: float | None = None

    fraud_channel: str | None = None

    transaction_time: str | None = None

    bank_name: str | None = None

    upi_app: str | None = None

    upi_id: str | None = None

    account_number: str | None = None

    phone_number: str | None = None

    email: str | None = None

    transaction_id: str | None = None

    description: str | None = None

    evidence: list[str] = Field(default_factory=list)

    answers: dict = Field(default_factory=dict)