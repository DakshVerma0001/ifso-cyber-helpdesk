from __future__ import annotations

import re

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

    @staticmethod
    def _normalize_word(word: str) -> str:
        """
        Lightweight stemming without external dependencies.

        scanned -> scan
        scanning -> scan
        shared -> share
        sharing -> share
        returns -> return
        codes -> code
        """

        word = word.lower()

        # Handle common verb forms
        if word.endswith("ing") and len(word) > 5:
            word = word[:-3]

        elif word.endswith("ed") and len(word) > 4:
            word = word[:-2]

        elif word.endswith("es") and len(word) > 4:
            word = word[:-2]

        elif word.endswith("s") and len(word) > 3:
            word = word[:-1]

        # Restore trailing "e" for words like:
        # shar -> share
        # receiv -> receive
        if word.endswith(("shar", "receiv", "verifi", "scann")):
            word += "e"

        return word

    def _keyword_match(
        self,
        message: str,
        keyword: str,
    ) -> bool:

        message = message.lower()
        keyword = keyword.lower()

        # Fast path
        if keyword in message:
            return True

        message_words = {
            self._normalize_word(word)
            for word in re.findall(
                r"[a-z0-9]+",
                message,
            )
        }

        keyword_words = [
            self._normalize_word(word)
            for word in re.findall(
                r"[a-z0-9]+",
                keyword,
            )
        ]

        if not keyword_words:
            return False

        matched = sum(
            word in message_words
            for word in keyword_words
        )

        # All words for single-word keywords,
        # 75% for multi-word keywords.
        threshold = (
            1.0
            if len(keyword_words) == 1
            else 0.75
        )

        return (
            matched / len(keyword_words)
        ) >= threshold

    def analyze(
        self,
        message: str,
    ) -> FraudAnalysisResult:

        message = normalize_text(message)

        patterns = PatternMatcher.detect(message)

        scorer = FraudScorer()

        for category in self.knowledge.get_categories():

            for rule in category.rules:

                for keyword in rule.keywords:

                    if self._keyword_match(
                        message,
                        keyword,
                    ):

                        scorer.add_score(
                            category=category.category,
                            weight=rule.weight,
                            explanation=rule.explanation,
                        )

        # Pattern based boosts

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

            confidence=min(
                score,
                MAX_CONFIDENCE,
            ),

            category=category_name,

            score=score,

            red_flags=sorted(
                set(scorer.flags)
            ),

            explanation=f"{len(scorer.flags)} fraud indicators matched.",
        )