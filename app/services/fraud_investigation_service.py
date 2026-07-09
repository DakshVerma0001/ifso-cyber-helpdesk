from __future__ import annotations

from app.services.classification_service import ClassificationService
from app.services.complaint_service import ComplaintService
from app.services.evidence_service import EvidenceService
from app.services.investigation_models import InvestigationReport

from app.services.evidence_collection_service import (
    EvidenceCollectionService,
)

class FraudInvestigationService:

    def __init__(self):

        self.classifier = ClassificationService()

        self.evidence_collection = EvidenceCollectionService()

        self.evidence = EvidenceService()

        self.complaint = ComplaintService()

    def investigate(
        self,
        *,
        description: str,
        incident_channel: str | None = None,
        loss_amount: float | None = None,
    ) -> InvestigationReport:

        classification = self.classifier.classify(
            description
        )

        evidence = self.evidence.extract(
            description
        )

        complaint = self.complaint.generate(

            classification=classification,

            evidence=evidence,

            description=description,

            incident_channel=incident_channel,

            loss_amount=loss_amount,
        )

        evidence_collection = self.evidence_collection.initialize(
            required=complaint.evidence_required
        )

        return InvestigationReport(

        fraud_type=classification.fraud_type,

        confidence=classification.confidence,

        severity=classification.severity,

        description=classification.description or "",

        explanation=classification.explanation,

        recommended_actions=classification.recommended_actions,

        evidence_required=complaint.evidence_required,

        evidence=evidence_collection,

        complaint=complaint,
    )