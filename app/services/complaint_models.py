from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ExtractedEntities(BaseModel):

    phone_numbers: list[str] = Field(default_factory=list)

    upi_ids: list[str] = Field(default_factory=list)

    emails: list[str] = Field(default_factory=list)

    urls: list[str] = Field(default_factory=list)

    transaction_ids: list[str] = Field(default_factory=list)

    bank_names: list[str] = Field(default_factory=list)

    amounts: list[float] = Field(default_factory=list)


class Complaint(BaseModel):

    complaint_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    fraud_type: str

    severity: str

    confidence: float

    incident_summary: str

    incident_channel: str | None = None

    loss_amount: float | None = None

    entities: ExtractedEntities

    recommended_actions: list[str] = Field(
        default_factory=list
    )

    evidence_required: list[str] = Field(
        default_factory=list
    )

    status: str = "READY_FOR_SUBMISSION"

    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )