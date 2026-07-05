from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = (
    BASE_DIR
    / "dataset"
    / "master"
    / "normalized_dataset.csv"
)

ARTIFACTS = (
    BASE_DIR
    / "artifacts"
    / "distilbert"
)

MODEL_NAME = "distilbert-base-uncased"

MAX_LENGTH = 256

TRAIN_BATCH_SIZE = 16

EVAL_BATCH_SIZE = 16

LEARNING_RATE = 2e-5

WEIGHT_DECAY = 0.01

EPOCHS = 4

RANDOM_STATE = 42