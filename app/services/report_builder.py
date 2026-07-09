from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel

from app.schemas.report import InvestigationReport


class ReportBuilder:
    def build(
        self,
        classification_result: Mapping[str, Any] | BaseModel | Any,
        knowledge_base: Any,
        evidence: Mapping[str, Any] | BaseModel | None,
        timeline: Sequence[Mapping[str, Any] | BaseModel],
        chatbot_answers: Sequence[Mapping[str, Any] | str] | None,
    ) -> dict[str, Any]:
        classification = self._coerce_mapping(classification_result)
        evidence_payload = self._coerce_mapping(evidence or {})
        timeline_payload = [self._coerce_mapping(item) for item in timeline]
        answers_payload = list(chatbot_answers or [])

        category = self._resolve_category(classification)
        knowledge = self._lookup_knowledge(knowledge_base, category)

        recommended_actions = self._merge_unique(
            classification.get("recommended_actions", []),
            knowledge.get("recommended_actions", []),
        )
        evidence_required = self._collect_evidence_required(knowledge)
        entities = self._build_entities(evidence_payload, answers_payload)
        loss_amount = self._resolve_loss_amount(evidence_payload, classification)

        report = InvestigationReport(
            summary=self._build_summary(
                category=category,
                classification=classification,
                loss_amount=loss_amount,
                evidence_count=len(evidence_payload),
                timeline_count=len(timeline_payload),
            ),
            fraud_type=category,
            severity=knowledge.get(
                "severity",
                classification.get("severity", "MEDIUM"),
            ),
            confidence=self._resolve_confidence(classification),
            loss_amount=loss_amount,
            entities=entities,
            timeline=timeline_payload,
            recommended_actions=recommended_actions,
            evidence_required=evidence_required,
            report_generated_at=datetime.now(timezone.utc),
        )

        return report.model_dump(mode="json")

    def _coerce_mapping(self, value: Mapping[str, Any] | BaseModel | Any) -> dict[str, Any]:
        if value is None:
            return {}

        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")

        if isinstance(value, Mapping):
            return dict(value)

        if hasattr(value, "model_dump"):
            return dict(value.model_dump(mode="json"))

        return {}

    def _resolve_category(self, classification: Mapping[str, Any]) -> str:
        return str(
            classification.get("fraud_type")
            or classification.get("category")
            or classification.get("label")
            or "UNKNOWN"
        )

    def _lookup_knowledge(self, knowledge_base: Any, category: str) -> dict[str, Any]:
        if knowledge_base is None:
            return {}

        if hasattr(knowledge_base, "get_categories"):
            items = knowledge_base.get_categories()
        elif isinstance(knowledge_base, Mapping) and "rules" in knowledge_base:
            items = [knowledge_base]
        else:
            items = knowledge_base

        if isinstance(items, Mapping):
            items = [items]

        for item in items or []:
            data = self._coerce_mapping(item)
            if str(data.get("category", "")).upper() == category.upper():
                return data

        return {}

    def _collect_evidence_required(self, knowledge: Mapping[str, Any]) -> list[str]:
        collected: list[str] = []

        for rule in knowledge.get("rules", []):
            rule_data = self._coerce_mapping(rule)
            collected.extend(rule_data.get("evidence_required", []))

        return self._merge_unique(collected)

    def _build_entities(
        self,
        evidence: Mapping[str, Any],
        chatbot_answers: Sequence[Mapping[str, Any] | str],
    ) -> dict[str, Any]:
        entities = dict(evidence)
        if chatbot_answers:
            entities["chatbot_answers"] = [
                answer if isinstance(answer, str) else self._coerce_mapping(answer)
                for answer in chatbot_answers
            ]
        return entities

    def _resolve_loss_amount(
        self,
        evidence: Mapping[str, Any],
        classification: Mapping[str, Any],
    ) -> str | None:
        for candidate in (
            evidence.get("amounts", []),
            classification.get("amount_lost"),
            classification.get("loss_amount"),
        ):
            if isinstance(candidate, Sequence) and not isinstance(candidate, (str, bytes, bytearray)):
                for value in candidate:
                    resolved = self._normalize_scalar(value)
                    if resolved:
                        return resolved
            else:
                resolved = self._normalize_scalar(candidate)
                if resolved:
                    return resolved
        return None

    def _resolve_confidence(self, classification: Mapping[str, Any]) -> float:
        value = classification.get("confidence", 0.0)
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            confidence = 0.0
        return confidence

    def _build_summary(
        self,
        *,
        category: str,
        classification: Mapping[str, Any],
        loss_amount: str | None,
        evidence_count: int,
        timeline_count: int,
    ) -> str:
        description = self._normalize_scalar(classification.get("description"))
        confidence = self._resolve_confidence(classification)
        parts = [
            f"{category} suspected with confidence {confidence:.2f}.",
        ]

        if description:
            parts.append(description)

        if loss_amount:
            parts.append(f"Estimated loss amount: {loss_amount}.")

        parts.append(f"Evidence items: {evidence_count}; timeline events: {timeline_count}.")
        return " ".join(parts)

    def _merge_unique(self, *sequences: Sequence[Any]) -> list[str]:
        seen: set[str] = set()
        merged: list[str] = []

        for sequence in sequences:
            for item in sequence or []:
                value = self._normalize_scalar(item)
                if not value:
                    continue
                key = value.lower()
                if key in seen:
                    continue
                seen.add(key)
                merged.append(value)

        return merged

    def _normalize_scalar(self, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            normalized = " ".join(value.split()).strip()
            return normalized or None
        return str(value)

