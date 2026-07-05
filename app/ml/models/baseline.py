from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class BaselineModel:

    @staticmethod
    def build() -> Pipeline:

        return Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        lowercase=True,
                        stop_words="english",
                        strip_accents="unicode",
                        sublinear_tf=True,
                        min_df=2,
                        max_df=0.95,
                        max_features=50000,
                        ngram_range=(1, 3),
)
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        random_state=42,
                        class_weight="balanced",
                        solver="saga",
                        C=2.0,
                        n_jobs=-1,
                    ),
                ),
            ]
        )