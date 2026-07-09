from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.evidence import EvidenceExtractionResult
from app.schemas.timeline import TimelineEvent


class ReportBuilderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    classification_result: dict[str, Any] = Field(default_factory=dict)
    knowledge_base: Any = None
    evidence: EvidenceExtractionResult = Field(default_factory=EvidenceExtractionResult)
    timeline: list[TimelineEvent] = Field(default_factory=list)
    chatbot_answers: list[dict[str, Any]] = Field(default_factory=list)


class InvestigationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    fraud_type: str
    severity: str
    confidence: float
    loss_amount: str | None = None
    entities: dict[str, Any] = Field(default_factory=dict)
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    evidence_required: list[str] = Field(default_factory=list)
    report_generated_at: datetime

