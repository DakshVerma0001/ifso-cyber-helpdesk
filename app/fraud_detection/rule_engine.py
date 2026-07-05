from app.fraud_detection.constants import (
    HIGH_THRESHOLD,
    MAX_CONFIDENCE,
    MEDIUM_THRESHOLD,
    RISK_SAFE,
    RISK_SCAM,
    RISK_SUSPICIOUS,
)
from app.fraud_detection.matcher import PatternMatcher
from app.fraud_detection.scorer import FraudScorer
from app.fraud_detection.schemas import FraudAnalysisResult
from app.fraud_detection.utils import normalize_text
from app.knowledge.manager import KnowledgeManager


class RuleEngine:
    def __init__(self) -> None:
        self.knowledge = KnowledgeManager()

    def analyze(self, message: str) -> FraudAnalysisResult:
        message = normalize_text(message)

        patterns = PatternMatcher.detect(message)

        scorer = FraudScorer()

        for category in self.knowledge.get_categories():

            for rule in category.rules:

                for keyword in rule.keywords:

                    if keyword.lower() in message:

                        scorer.add_score(
                            category=category.category,
                            weight=rule.weight,
                            explanation=rule.explanation,
                        )

        if patterns["urls"]:
            scorer.add_score(
                category="COMMON",
                weight=10,
                explanation="Message contains a URL.",
            )

        if patterns["upi_ids"]:
            scorer.add_score(
                category="UPI_FRAUD",
                weight=20,
                explanation="Message contains a UPI ID.",
            )

        if patterns["phones"]:
            scorer.add_score(
                category="COMMON",
                weight=5,
                explanation="Message contains a phone number.",
            )

        category_name, score = scorer.highest_category()

        if category_name is None:
            return FraudAnalysisResult(
                label=RISK_SAFE,
                confidence=95,
                category="SAFE",
                score=0,
                red_flags=[],
                explanation="No fraud indicators detected.",
            )

        if score >= HIGH_THRESHOLD:
            label = RISK_SCAM
        elif score >= MEDIUM_THRESHOLD:
            label = RISK_SUSPICIOUS
        else:
            label = RISK_SAFE

        return FraudAnalysisResult(
            label=label,
            confidence=min(score, MAX_CONFIDENCE),
            category=category_name,
            score=score,
            red_flags=sorted(set(scorer.flags)),
            explanation=f"{len(scorer.flags)} fraud indicators matched.",
        )