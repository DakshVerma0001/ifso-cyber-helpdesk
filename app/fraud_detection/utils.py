import re


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(r"\n", " ", text)

    text = re.sub(r"\t", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()