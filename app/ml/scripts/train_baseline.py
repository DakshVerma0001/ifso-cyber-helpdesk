from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.ml.training.evaluator import ModelEvaluator
from app.ml.training.trainer import ModelTrainer


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = (
    BASE_DIR
    / "dataset"
    / "master"
    / "normalized_dataset.csv"
)

OUTPUT = (
    BASE_DIR
    / "artifacts"
)


SUPPORTED_LABELS = {

    "UPI_FRAUD",

    "BANKING_FRAUD",

    "CARD_SIM_SWAP_FRAUD",

    "EWALLET_FRAUD",

    "PHISHING",

    "SMISHING",

    "VISHING",

    "JOB_SCAM",

    "ROMANCE_SCAM",

    "INVESTMENT_SCAM",

    "DIGITAL_ARREST",

    "RENTAL_SCAM",

    "ACCOUNT_TAKEOVER",

    "SOCIAL_ENGINEERING",

    "FAKE_PROFILE",

    "STOCK_TIP_SCAM",

    "CRYPTO_FRAUD",

    "OTHER",

}


def main():

    df = pd.read_csv(DATASET)

    df = df[
        df["fraud_label"].isin(
            SUPPORTED_LABELS
        )
    ]

    print()

    print(f"Training Samples : {len(df)}")

    trainer = ModelTrainer(df)

    (
        model,
        encoder,
        X_test,
        y_test,
    ) = trainer.train()

    OUTPUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    trainer.save(
        model,
        encoder,
        OUTPUT,
    )

    ModelEvaluator.evaluate(
        model,
        X_test,
        y_test,
        encoder,
    )

    print()

    print("Artifacts saved to")

    print(OUTPUT)


if __name__ == "__main__":

    main()