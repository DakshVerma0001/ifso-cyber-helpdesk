from __future__ import annotations

from pathlib import Path

import joblib
import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from app.ml.bert.config import ARTIFACTS


class BertPredictor:

    def __init__(self):

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            ARTIFACTS
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(ARTIFACTS)
            .to(self.device)
        )

        self.model.eval()

        self.encoder = joblib.load(
            ARTIFACTS / "label_encoder.pkl"
        )

    @torch.no_grad()
    def predict(self, text: str):

        encoded = self.tokenizer(

            text,

            return_tensors="pt",

            truncation=True,

            padding=True,

            max_length=256,
        )

        encoded = {
            k: v.to(self.device)
            for k, v in encoded.items()
        }

        outputs = self.model(**encoded)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1,
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1,
        )

        fraud_type = self.encoder.inverse_transform(
            prediction.cpu().numpy()
        )[0]

        return {

            "fraud_type": fraud_type,

            "confidence": round(
                confidence.item(),
                4,
            ),
        }