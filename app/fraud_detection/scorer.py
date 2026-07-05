from collections import defaultdict


class FraudScorer:

    def __init__(self):

        self.scores = defaultdict(int)

        self.flags = []

    def add_score(
        self,
        category,
        weight,
        explanation,
    ):

        self.scores[category] += weight

        self.flags.append(explanation)

    def highest_category(self):

        if not self.scores:
            return None, 0

        category = max(
            self.scores,
            key=self.scores.get,
        )

        return category, self.scores[category]