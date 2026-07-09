from __future__ import annotations

from app.decision.confidence import (
    ConfidenceAnalyzer,
)


class DecisionEngine:

    def resolve(
        self,
        message: str,
        ml_result: dict,
        rule_result,
    ) -> dict:

        ml_category = ml_result["fraud_type"]

        ml_confidence = ml_result["confidence"]

        ml_level = ConfidenceAnalyzer.level(
            ml_confidence
        )

        rule_category = rule_result.category

        rule_score = rule_result.score

        # Strong rule match
        if rule_score >= 70:

            return {
                "fraud_type": rule_category,
                "confidence": 0.98,
                "source": "RULE_ENGINE",
            }

        # Strong ML prediction
        if (
            ml_level.value == "HIGH"
            and rule_score < 30
        ):

            return {
                "fraud_type": ml_category,
                "confidence": ml_confidence,
                "source": "DISTILBERT",
            }

        # Agreement between ML and Rules
        if (
            rule_category
            and rule_category == ml_category
        ):

            return {
                "fraud_type": ml_category,
                "confidence": max(
                    ml_confidence,
                    0.90,
                ),
                "source": "HYBRID",
            }

        # Medium confidence + useful rules
        if (
            ml_level.value == "MEDIUM"
            and rule_score >= 30
        ):

            return {
                "fraud_type": rule_category,
                "confidence": 0.90,
                "source": "HYBRID",
            }

        # Weak ML -> trust rules if available
        if (
            ml_level.value == "LOW"
            and rule_category
            and rule_category != "SAFE"
        ):

            return {
                "fraud_type": rule_category,
                "confidence": 0.85,
                "source": "RULE_ENGINE",
            }

        return {
            "fraud_type": ml_category,
            "confidence": ml_confidence,
            "source": "DISTILBERT",
        }