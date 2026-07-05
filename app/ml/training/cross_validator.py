from __future__ import annotations

from sklearn.model_selection import cross_val_score


class CrossValidator:

    @staticmethod
    def evaluate(model, X, y):

        scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring="f1_weighted",
            n_jobs=-1,
        )

        print("\nCross Validation")
        print("-" * 40)
        print(scores)
        print(f"\nMean F1 : {scores.mean():.4f}")