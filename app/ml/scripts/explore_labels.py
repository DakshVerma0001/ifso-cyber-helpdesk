from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "cleaned_dataset.csv"
)


def main() -> None:

    df = pd.read_csv(DATASET_PATH)

    print("\nUnique Categories\n")
    print(df["category"].value_counts())

    print("\nUnique Sub Categories\n")
    print(df["sub_category"].value_counts())

    output = (
        BASE_DIR
        / "dataset"
        / "reports"
        / "unique_subcategories.csv"
    )

    (
        df["sub_category"]
        .value_counts()
        .rename_axis("sub_category")
        .reset_index(name="count")
        .to_csv(output, index=False)
    )

    print(f"\nSaved to:\n{output}")


if __name__ == "__main__":
    main()