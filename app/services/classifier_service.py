from functools import lru_cache

from app.fraud_detection.rule_engine import RuleEngine


class ClassifierService:
    def __init__(self) -> None:
        self.engine = RuleEngine()

    def classify(self, message: str):
        return self.engine.analyze(message)


@lru_cache
def get_classifier_service() -> ClassifierService:
    return ClassifierService()