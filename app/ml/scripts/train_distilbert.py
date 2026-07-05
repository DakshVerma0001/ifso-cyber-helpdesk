from pathlib import Path

import joblib

from app.ml.bert.config import ARTIFACTS
from app.ml.bert.dataset import FraudDataset
from app.ml.bert.model import FraudClassifier
from app.ml.bert.trainer import FraudTrainer


def main():

    dataset = FraudDataset()

    train, test, encoder = dataset.prepare()

    model = FraudClassifier.build(
        len(encoder.classes_)
    )

    trainer = FraudTrainer.build(

        model=model,

        tokenizer=dataset.tokenizer,

        train_dataset=train,

        test_dataset=test,
    )

    trainer.train()

    trainer.evaluate()

    ARTIFACTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    trainer.save_model(
        ARTIFACTS
    )

    dataset.tokenizer.save_pretrained(
        ARTIFACTS
    )

    joblib.dump(
        encoder,
        ARTIFACTS / "label_encoder.pkl",
    )

    print()

    print("Training completed.")

    print()

    print(f"Artifacts saved to {ARTIFACTS}")


if __name__ == "__main__":

    main()