from __future__ import annotations

import json
import random
from pathlib import Path

import pandas as pd

from app.ml.templates.complaint_templates import (
    COMPLAINT_TEMPLATES,
)

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = (
    BASE_DIR.parent
    / "knowledge"
    / "red_flags"
)

OUTPUT_FILE = (
    BASE_DIR
    / "dataset"
    / "synthetic"
    / "synthetic_dataset.csv"
)


class SyntheticDatasetGenerator:

    def __init__(self):

        self.samples = []

    def generate(self):

        random.seed(42)

        for file in KNOWLEDGE_DIR.glob("*.json"):

            with open(
                file,
                encoding="utf-8"
            ) as fp:

                category = json.load(fp)

            fraud = category["category"]

            for rule in category["rules"]:

                for keyword in rule["keywords"]:

                    for template in COMPLAINT_TEMPLATES:

                        for i in range(30):
                            template = random.choice(COMPLAINT_TEMPLATES)

                            complaint = template.format(
                                keyword=keyword 
                            )

                            self.samples.append(
                                {
                                    "text": complaint,
                                    "fraud_label": fraud,
                                    "source": "SYNTHETIC",
                                }
                            )
        return pd.DataFrame(
            self.samples
        )

    def save(self):

        df = self.generate()

        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8",
        )

        print()

        print(
            f"Generated {len(df)} synthetic samples."
        )

        print()

        print(
            df["fraud_label"]
            .value_counts()
        )

        print()

        print(
            f"Saved to {OUTPUT_FILE}"
        )


def main():

    generator = SyntheticDatasetGenerator()

    generator.save()


if __name__ == "__main__":

    main()