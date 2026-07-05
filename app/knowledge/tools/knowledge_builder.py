from __future__ import annotations

from collections import defaultdict

from app.knowledge.loader import KnowledgeLoader
from app.knowledge.models import FraudCategory
from app.knowledge.validator import KnowledgeValidator


class KnowledgeBuilder:

    def __init__(self) -> None:

        self.categories: list[FraudCategory] = [
            KnowledgeValidator.validate(item)
            for item in KnowledgeLoader.load_directory("red_flags")
        ]

    def validate(self) -> None:

        self._validate_categories()

        self._validate_rule_ids()

        self._validate_duplicate_keywords()

        print("\nKnowledge base validation completed successfully.\n")

    def _validate_categories(self) -> None:

        categories = set()

        for category in self.categories:

            if category.category in categories:

                raise ValueError(
                    f"Duplicate category '{category.category}'."
                )

            categories.add(category.category)

    def _validate_rule_ids(self) -> None:

        ids = set()

        for category in self.categories:

            for rule in category.rules:

                if rule.id in ids:

                    raise ValueError(
                        f"Duplicate rule id '{rule.id}'."
                    )

                ids.add(rule.id)

    def _validate_duplicate_keywords(self) -> None:

        keyword_map = defaultdict(list)

        for category in self.categories:

            for rule in category.rules:

                for keyword in rule.keywords:

                    keyword_map[
                        keyword.lower().strip()
                    ].append(rule.id)

        duplicates = {
            keyword: rules
            for keyword, rules in keyword_map.items()
            if len(rules) > 1
        }

        if duplicates:

            print("\nDuplicate keywords detected:\n")

            for keyword, rules in duplicates.items():

                print(
                    f"{keyword} -> {', '.join(rules)}"
                )

            print()