from __future__ import annotations

import pandas as pd

from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer

from app.ml.bert.config import (
    DATASET,
    MODEL_NAME,
    MAX_LENGTH,
    RANDOM_STATE,
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
}


class FraudDataset:

    def __init__(self):

        self.df = pd.read_csv(DATASET)

        self.encoder = LabelEncoder()

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

    def prepare(self):

        # Remove missing rows
        self.df = self.df.dropna()

        # Keep only fraud categories supported by our chatbot
        self.df = self.df[
            self.df["fraud_label"].isin(
                SUPPORTED_LABELS
            )
        ]

        # Remove classes with fewer than 2 samples
        counts = self.df["fraud_label"].value_counts()

        valid_labels = counts[counts >= 2].index

        self.df = self.df[
            self.df["fraud_label"].isin(valid_labels)
        ]

        # Development mode (30% dataset)
        # Remove this line for final production training
        self.df = self.df.sample(
            frac=0.30,
            random_state=RANDOM_STATE,
        )

        self.df = self.df.reset_index(
            drop=True
        )

        labels = self.encoder.fit_transform(
            self.df["fraud_label"]
        )

        train_texts, test_texts, train_labels, test_labels = train_test_split(
            self.df["text"],
            labels,
            test_size=0.20,
            stratify=labels,
            random_state=RANDOM_STATE,
        )

        train = Dataset.from_dict(
            {
                "text": train_texts.tolist(),
                "label": train_labels.tolist(),
            }
        )

        test = Dataset.from_dict(
            {
                "text": test_texts.tolist(),
                "label": test_labels.tolist(),
            }
        )

        train = train.map(
            self.tokenize,
            batched=True,
        )

        test = test.map(
            self.tokenize,
            batched=True,
        )

        return (
            train,
            test,
            self.encoder,
        )

    def tokenize(self, examples):

        return self.tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
        )