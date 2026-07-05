from __future__ import annotations

from app.knowledge.loader import KnowledgeLoader
from app.knowledge.validator import KnowledgeValidator


class KnowledgeManager:

    def __init__(self):

        self.categories = []

        for item in KnowledgeLoader.load_directory(
            "red_flags"
        ):

            self.categories.append(
                KnowledgeValidator.validate(item)
            )

    def get_categories(self):

        return self.categories