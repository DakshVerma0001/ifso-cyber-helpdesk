from app.knowledge.models import FraudCategory


class KnowledgeValidator:

    @staticmethod
    def validate(data: dict) -> FraudCategory:

        category = FraudCategory.model_validate(data)

        KnowledgeValidator._validate_rule_ids(category)

        return category

    @staticmethod
    def _validate_rule_ids(
        category: FraudCategory,
    ) -> None:

        ids = set()

        for rule in category.rules:

            if rule.id in ids:

                raise ValueError(
                    f"Duplicate rule id '{rule.id}' in {category.category}"
                )

            ids.add(rule.id)