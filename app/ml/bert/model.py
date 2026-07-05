from transformers import AutoModelForSequenceClassification

from app.ml.bert.config import MODEL_NAME


class FraudClassifier:

    @staticmethod
    def build(num_labels: int):

        return AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=num_labels,
        )