from __future__ import annotations

import json
from pathlib import Path


class AwarenessManager:

    def __init__(self):

        self.base_path = (
            Path(__file__).parent / "awareness"
        )

        self.data = []

        self._load()

    def _load(self):

        self.data.clear()

        for file in self.base_path.glob("*.json"):

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                self.data.append(
                    json.load(f)
                )

    def find(
        self,
        question: str,
    ):

        question = question.lower()

        best_match = None

        best_score = 0

        for item in self.data:

            score = 0

            for keyword in item.get(
                "keywords",
                [],
            ):

                if keyword.lower() in question:

                    score += 2

            for sample in item.get(
                "common_questions",
                [],
            ):

                if sample.lower() in question:

                    score += 3

            if score > best_score:

                best_score = score

                best_match = item

        return best_match