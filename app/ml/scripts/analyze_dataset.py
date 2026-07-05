from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR /
    "dataset" /
    "external" /
    "cleaned_train.csv"
)

REPORT_PATH = (
    BASE_DIR /
    "dataset" /
    "reports" /
    "dataset_report.txt"
)


class DatasetAnalyzer:

    def __init__(self) -> None:

        self.df = pd.read_csv(DATASET_PATH)

    def generate_report(self) -> None:

        lines: list[str] = []

        lines.append("IFSO Cyber Fraud Dataset Report")
        lines.append("=" * 60)
        lines.append("")

        lines.append(f"Rows : {len(self.df)}")
        lines.append(f"Columns : {len(self.df.columns)}")
        lines.append("")

        lines.append("Columns")
        lines.append("-" * 30)

        for column in self.df.columns:

            lines.append(column)

        lines.append("")
        lines.append("Missing Values")
        lines.append("-" * 30)

        for column in self.df.columns:

            lines.append(
                f"{column}: {self.df[column].isna().sum()}"
            )

        lines.append("")
        lines.append(
            f"Duplicate Rows : {self.df.duplicated().sum()}"
        )

        lines.append("")
        lines.append("Category Distribution")
        lines.append("-" * 30)

        category_column = self.df.columns[0]

        distribution = (
            self.df[category_column]
            .value_counts()
            .sort_values(
                ascending=False
            )
        )

        for category, count in distribution.items():

            lines.append(
                f"{category}: {count}"
            )

        text_column = self.df.columns[2]

        text_lengths = (
            self.df[text_column]
            .fillna("")
            .astype(str)
        )

        lines.append("")
        lines.append("Text Statistics")
        lines.append("-" * 30)

        lines.append(
            f"Average Characters : {text_lengths.str.len().mean():.2f}"
        )

        lines.append(
            f"Maximum Characters : {text_lengths.str.len().max()}"
        )

        lines.append(
            f"Minimum Characters : {text_lengths.str.len().min()}"
        )

        word_counts = text_lengths.str.split().str.len()

        lines.append(
            f"Average Words : {word_counts.mean():.2f}"
        )

        REPORT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        REPORT_PATH.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        print("\n".join(lines))


def main() -> None:

    analyzer = DatasetAnalyzer()

    analyzer.generate_report()


if __name__ == "__main__":

    main()