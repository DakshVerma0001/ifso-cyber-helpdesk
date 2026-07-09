from __future__ import annotations

from functools import lru_cache

from app.decision.decision_engine import DecisionEngine
from app.fraud_detection.rule_engine import RuleEngine
from app.knowledge.manager import KnowledgeManager
from app.ml.bert.predictor import BertPredictor
from app.services.schemas import ClassificationResponse


class ClassificationService:

    def __init__(self):

        self.predictor = BertPredictor()

        self.rule_engine = RuleEngine()

        self.knowledge = KnowledgeManager()

        self.decision = DecisionEngine()

    def classify(
        self,
        message: str,
    ) -> ClassificationResponse:

        # AI Prediction
        ml = self.predictor.predict(message)

        # Rule-Based Analysis
        rules = self.rule_engine.analyze(message)

        # Final Decision
        decision = self.decision.resolve(
            message=message,
            ml_result=ml,
            rule_result=rules,
        )

        fraud_type = decision["fraud_type"]

        confidence = decision["confidence"]

        source = decision["source"]

        # Lookup knowledge base
        knowledge = self._knowledge(
            fraud_type
        )

        return ClassificationResponse(

            fraud_type=fraud_type,

            confidence=round(
                confidence,
                4,
            ),

            source=source,

            severity=knowledge.get(
                "severity",
                "MEDIUM",
            ),

            description=knowledge.get(
                "description"
            ),

            explanation=rules.red_flags,

            recommended_actions=knowledge.get(
                "recommended_actions",
                [],
            ),
        )

    def _knowledge(
        self,
        category: str,
    ):

        for item in self.knowledge.get_categories():

            if item.category == category:

                return item.model_dump()

        return {}


@lru_cache
def get_classification_service():

    return ClassificationService()