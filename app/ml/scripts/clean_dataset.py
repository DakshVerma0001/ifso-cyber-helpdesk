from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "external"
    / "cleaned_train.csv"
)

OUTPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "cleaned_dataset.csv"
)


class DatasetCleaner:

    def __init__(self) -> None:

        self.df = pd.read_csv(INPUT_DATASET)

    @staticmethod
    def normalize_text(text: str) -> str:

        if pd.isna(text):
            return ""

        text = str(text)

        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def clean(self) -> pd.DataFrame:

        print(f"Original Rows : {len(self.df)}")

        # Remove rows with missing text
        self.df = self.df.dropna(subset=["text"])

        # Normalize complaint text
        self.df["text"] = self.df["text"].apply(
            self.normalize_text
        )

        # Remove very short complaints
        self.df = self.df[
            self.df["text"].str.len() >= 10
        ]

        # Remove duplicate complaints
        self.df = self.df.drop_duplicates(
            subset=["text"]
        )

        # Remove duplicate complete rows
        self.df = self.df.drop_duplicates()

        # Remove rows with empty categories
        self.df = self.df.dropna(
            subset=["category", "sub_category"]
        )

        # Reset indices
        self.df.reset_index(
            drop=True,
            inplace=True,
        )

        print(f"Cleaned Rows : {len(self.df)}")

        return self.df

    def save(self) -> None:

        cleaned = self.clean()

        OUTPUT_DATASET.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cleaned.to_csv(
            OUTPUT_DATASET,
            index=False,
            encoding="utf-8",
        )

        print()
        print(f"Dataset saved to:")
        print(OUTPUT_DATASET)


def main() -> None:

    cleaner = DatasetCleaner()

    cleaner.save()


if __name__ == "__main__":

    main()