from __future__ import annotations

import evaluate
import numpy as np

from transformers import (
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from app.ml.bert.config import (
    ARTIFACTS,
    EPOCHS,
    EVAL_BATCH_SIZE,
    LEARNING_RATE,
    TRAIN_BATCH_SIZE,
    WEIGHT_DECAY,
)


accuracy_metric = evaluate.load("accuracy")
precision_metric = evaluate.load("precision")
recall_metric = evaluate.load("recall")
f1_metric = evaluate.load("f1")


class FraudTrainer:

    @staticmethod
    def compute_metrics(eval_pred):

        logits, labels = eval_pred

        predictions = np.argmax(
            logits,
            axis=1,
        )

        accuracy = accuracy_metric.compute(
            predictions=predictions,
            references=labels,
        )

        precision = precision_metric.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )

        recall = recall_metric.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )

        f1 = f1_metric.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )

        return {
            "accuracy": accuracy["accuracy"],
            "precision": precision["precision"],
            "recall": recall["recall"],
            "f1": f1["f1"],
        }

    @staticmethod
    def build(
        model,
        tokenizer,
        train_dataset,
        test_dataset,
    ):

        args = TrainingArguments(

            output_dir=str(ARTIFACTS),

            learning_rate=LEARNING_RATE,

            per_device_train_batch_size=TRAIN_BATCH_SIZE,

            per_device_eval_batch_size=EVAL_BATCH_SIZE,

            num_train_epochs=EPOCHS,

            weight_decay=WEIGHT_DECAY,

            evaluation_strategy="epoch",

            save_strategy="epoch",

            logging_strategy="epoch",

            load_best_model_at_end=True,

            metric_for_best_model="f1",

            greater_is_better=True,

            report_to="none",
        )

        trainer = Trainer(

            model=model,

            args=args,

            train_dataset=train_dataset,

            eval_dataset=test_dataset,

            tokenizer=tokenizer,

            data_collator=DataCollatorWithPadding(
                tokenizer
            ),

            compute_metrics=FraudTrainer.compute_metrics,
        )

        return trainer