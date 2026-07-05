from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

REAL_DATASET = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "cleaned_dataset.csv"
)

SYNTHETIC_DATASET = (
    BASE_DIR
    / "dataset"
    / "synthetic"
    / "synthetic_dataset.csv"
)

OUTPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "master"
    / "master_dataset.csv"
)


class DatasetMerger:

    def load_real(self) -> pd.DataFrame:

        df = pd.read_csv(REAL_DATASET)

        df = df.rename(
            columns={
                "sub_category": "fraud_label"
            }
        )

        df = df[
            [
                "text",
                "fraud_label",
            ]
        ]

        df["source"] = "REAL"

        return df

    def load_synthetic(self) -> pd.DataFrame:

        df = pd.read_csv(SYNTHETIC_DATASET)

        df = df[
            [
                "text",
                "fraud_label",
                "source",
            ]
        ]

        return df

    def merge(self):

        real = self.load_real()

        synthetic = self.load_synthetic()

        merged = pd.concat(
            [
                real,
                synthetic,
            ],
            ignore_index=True,
        )

        merged = merged.drop_duplicates(
            subset=["text", "fraud_label"]
        )

        merged = merged[
            ~merged["fraud_label"].isin(
                [
                    "COMMON",
                    "FRAUD_RED_FLAGS",
                ]
            )
        ]

        merged = merged.sample(
            frac=1,
            random_state=42,
        ).reset_index(drop=True)

        OUTPUT_DATASET.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        merged.to_csv(
            OUTPUT_DATASET,
            index=False,
            encoding="utf-8",
        )

        print()

        print("Master Dataset")

        print("-" * 40)

        print(merged.head())

        print()

        print(f"Rows : {len(merged)}")

        print()

        print(merged["source"].value_counts())

        print()

        print(merged["fraud_label"].value_counts())

        print()

        print(f"Saved to:\n{OUTPUT_DATASET}")


def main():

    DatasetMerger().merge()


if __name__ == "__main__":

    main()