from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "cleaned_dataset.csv"
)

OUTPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "mapped_dataset.csv"
)


LABEL_MAPPING = {

    "UPI Related Frauds": "UPI_FRAUD",

    "Debit/Credit Card Fraud": "CARD_FRAUD",

    "Internet Banking Related Fraud": "BANKING_FRAUD",

    "Aadhaar-enabled Payment System (AePS) Fraud": "AEPS_FRAUD",

    "EWallet Related Fraud": "EWALLET_FRAUD",

    "QR Code Fraud": "QR_CODE_FRAUD",

    "OTP Fraud": "OTP_FRAUD",

    "Phishing": "PHISHING",

    "Fake Profile": "FAKE_PROFILE",

    "Profile Hacking Identity Theft": "ACCOUNT_TAKEOVER",

    "Cyber Bullying Stalking Sexting": "CYBER_BULLYING",

    "Online Job Fraud": "JOB_SCAM",

    "Matrimonial Romance Scam Honey Trap": "ROMANCE_SCAM",

    "Investment Scam Trading Scam": "INVESTMENT_SCAM",

    "Online Shopping E-commerce Frauds": "ECOMMERCE_FRAUD",

    "Advance Fee Fraud": "ADVANCE_FEE_FRAUD",

    "Lottery Fraud": "LOTTERY_SCAM",

    "Courier Parcel Scam": "PARCEL_SCAM",

    "Tech Support Scam": "TECH_SUPPORT_SCAM",

    "SIM Swap Fraud": "SIM_SWAP",

    "Crypto Currency Fraud": "CRYPTO_FRAUD",

    "Online Gambling Betting": "GAMBLING_SCAM",

}

class LabelMapper:

    def __init__(self):

        self.df = pd.read_csv(INPUT_DATASET)

    def map_labels(self):

        self.df["fraud_label"] = (
            self.df["sub_category"]
            .map(LABEL_MAPPING)
            .fillna("OTHER")
        )

        return self.df

    def save(self):

        mapped = self.map_labels()

        OUTPUT_DATASET.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        mapped.to_csv(
            OUTPUT_DATASET,
            index=False,
            encoding="utf-8",
        )

        print()

        print("Mapped Dataset Statistics")

        print("-" * 40)

        print(
            mapped["fraud_label"]
            .value_counts()
        )

        print()

        print(
            f"Saved to {OUTPUT_DATASET}"
        )


def main():

    mapper = LabelMapper()

    mapper.save()


if __name__ == "__main__":

    main()