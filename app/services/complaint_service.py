from __future__ import annotations

from app.services.schemas import ClassificationResponse
from app.services.complaint_models import (
    Complaint,
    ExtractedEntities,
)
from app.services.evidence_service import EvidenceExtractionResult
from app.knowledge.manager import KnowledgeManager


class ComplaintService:

    def __init__(self):

        self.knowledge = KnowledgeManager()

    def generate(
        self,
        *,
        classification: ClassificationResponse,
        evidence: EvidenceExtractionResult,
        description: str,
        incident_channel: str | None = None,
        loss_amount: float | None = None,
    ) -> Complaint:

        entities = ExtractedEntities(

            phone_numbers=evidence.phone_numbers,

            upi_ids=evidence.upi_ids,

            emails=evidence.emails,

            urls=evidence.urls,

            transaction_ids=evidence.transaction_ids,

            bank_names=evidence.bank_names,

            amounts=[
                float(amount)
                for amount in evidence.amounts
            ],
        )

        if loss_amount is None and entities.amounts:

            loss_amount = max(
                entities.amounts
            )

        return Complaint(

            fraud_type=classification.fraud_type,

            severity=classification.severity,

            confidence=classification.confidence,

            incident_summary=description,

            incident_channel=incident_channel,

            loss_amount=loss_amount,

            entities=entities,

            recommended_actions=classification.recommended_actions,

            evidence_required=self._get_required_evidence(
                classification.fraud_type
            ),
        )

    def _get_required_evidence(
        self,
        category: str,
    ) -> list[str]:

        evidence = set()

        for item in self.knowledge.get_categories():

            if item.category != category:
                continue

            for rule in item.rules:

                for ev in getattr(
                    rule,
                    "evidence_required",
                    [],
                ):

                    evidence.add(ev)

        return sorted(evidence)