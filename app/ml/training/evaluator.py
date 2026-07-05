from __future__ import annotations

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


class ModelEvaluator:

    @staticmethod
    def evaluate(
        model,
        X_test,
        y_test,
        encoder,
    ) -> None:

        predictions = model.predict(X_test)

        print("\n")
        print("=" * 60)
        print("Baseline Model Evaluation")
        print("=" * 60)

        print(
            f"Accuracy : {accuracy_score(y_test, predictions):.4f}"
        )

        print(
            f"Precision : {precision_score(y_test, predictions, average='weighted'):.4f}"
        )

        print(
            f"Recall : {recall_score(y_test, predictions, average='weighted'):.4f}"
        )

        print(
            f"F1 Score : {f1_score(y_test, predictions, average='weighted'):.4f}"
        )

        print("\nClassification Report\n")

        print(
            classification_report(
                y_test,
                predictions,
                target_names=encoder.classes_,
                zero_division=0,
            )
        )

        print("\nConfusion Matrix\n")

        print(
            confusion_matrix(
                y_test,
                predictions,
            )
        )