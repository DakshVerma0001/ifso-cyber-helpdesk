from __future__ import annotations

from pydantic import BaseModel

from app.services.complaint_models import Complaint
from app.services.evidence_models import EvidenceCollection

class InvestigationReport(BaseModel):

    fraud_type: str

    confidence: float

    severity: str

    description: str

    explanation: list[str]

    recommended_actions: list[str]

    evidence_required: list[str]

    evidence: EvidenceCollection

    complaint: Complaint