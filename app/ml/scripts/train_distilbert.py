from pathlib import Path
import os

import joblib

from app.ml.bert.config import ARTIFACTS
from app.ml.bert.dataset import FraudDataset
from app.ml.bert.model import FraudClassifier
from app.ml.bert.trainer import FraudTrainer


def main():

    print("=" * 60)
    print("IFSO Fraud Detection Model Training")
    print("=" * 60)
    print()

    print(f"Dataset: {os.getenv('DATASET_PATH', 'Local Dataset')}")
    print(f"Artifacts Directory: {ARTIFACTS}")
    print()

    dataset = FraudDataset()

    train, test, encoder = dataset.prepare()

    print(f"Training Samples: {len(train)}")
    print(f"Validation Samples: {len(test)}")
    print(f"Fraud Categories: {len(encoder.classes_)}")
    print()

    model = FraudClassifier.build(
        len(encoder.classes_)
    )

    trainer = FraudTrainer.build(

        model=model,

        tokenizer=dataset.tokenizer,

        train_dataset=train,

        eval_dataset=test,
    )

    print("Starting Training...")
    print()

    trainer.train()

    print()
    print("Evaluating Best Model...")
    print()

    metrics = trainer.evaluate()

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
    print("=" * 60)
    print("Training Completed Successfully")
    print("=" * 60)
    print()

    print(metrics)

    print()

    print(f"Artifacts saved to {ARTIFACTS}")


if __name__ == "__main__":

    main()