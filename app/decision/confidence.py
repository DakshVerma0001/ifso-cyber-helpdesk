from enum import Enum


class ConfidenceLevel(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class ConfidenceAnalyzer:

    @staticmethod
    def level(score: float) -> ConfidenceLevel:

        if score >= 0.85:
            return ConfidenceLevel.HIGH

        if score >= 0.60:
            return ConfidenceLevel.MEDIUM

        return ConfidenceLevel.LOW