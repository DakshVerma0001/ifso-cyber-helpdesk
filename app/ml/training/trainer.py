from __future__ import annotations

import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from app.ml.models.baseline import BaselineModel


class ModelTrainer:

    def __init__(self, dataframe):

        self.df = dataframe

        self.encoder = LabelEncoder()

    def split(self):

        X = self.df["text"]

        y = self.encoder.fit_transform(
            self.df["fraud_label"]
        )

        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

    def train(self):

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = self.split()

        model = BaselineModel.build()

        model.fit(
            X_train,
            y_train,
        )

        return (
            model,
            self.encoder,
            X_test,
            y_test,
        )

    @staticmethod
    def save(model, encoder, output_dir):

        joblib.dump(
            model,
            output_dir / "baseline_model.pkl",
        )

        joblib.dump(
            encoder,
            output_dir / "label_encoder.pkl",
        )