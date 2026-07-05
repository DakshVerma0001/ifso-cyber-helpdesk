import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent


class KnowledgeLoader:

    @staticmethod
    def load(relative_path: str) -> Any:
        path = BASE_DIR / relative_path

        with open(path, encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def load_directory(relative_directory: str) -> list[dict]:
        directory = BASE_DIR / relative_directory

        knowledge = []

        for file in sorted(directory.glob("*.json")):

            print(f"Loading: {file}")

            try:
                with open(file, encoding="utf-8") as fp:
                    knowledge.append(json.load(fp))

            except Exception as exc:
                print(f"Failed: {file}")
                raise

        return knowledge