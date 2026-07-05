from __future__ import annotations

import json
from pathlib import Path

from app.knowledge.models import FraudCategory

BASE_DIR = Path(__file__).resolve().parent.parent
RED_FLAGS_DIR = BASE_DIR / "red_flags"


class KnowledgeGenerator:

    @staticmethod
    def write(category: FraudCategory) -> None:

        output = RED_FLAGS_DIR / f"{category.category.lower()}.json"

        with open(output, "w", encoding="utf-8") as fp:

            json.dump(
                category.model_dump(),
                fp,
                indent=2,
                ensure_ascii=False,
            )

        print(f"Generated {output.name}")