from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.ml.constants.label_mapping import LABEL_MAPPING


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "master"
    / "master_dataset.csv"
)

OUTPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "master"
    / "normalized_dataset.csv"
)


class LabelNormalizer:

    def __init__(self):

        self.df = pd.read_csv(INPUT_DATASET)

    def normalize(self):

        self.df["fraud_label"] = (
            self.df["fraud_label"]
            .replace(LABEL_MAPPING)
        )

        self.df["fraud_label"] = (
            self.df["fraud_label"]
            .fillna("OTHER")
        )

        self.df = self.df.drop_duplicates()

        self.df = self.df.reset_index(
            drop=True
        )

        return self.df

    def save(self):

        normalized = self.normalize()

        OUTPUT_DATASET.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        normalized.to_csv(
            OUTPUT_DATASET,
            index=False,
            encoding="utf-8",
        )

        print()

        print("Normalized Labels")

        print("-" * 40)

        print(
            normalized["fraud_label"]
            .value_counts()
        )

        print()

        print(
            f"Rows : {len(normalized)}"
        )

        print()

        print(
            f"Saved to:\n{OUTPUT_DATASET}"
        )


def main():

    LabelNormalizer().save()


if __name__ == "__main__":

    main()