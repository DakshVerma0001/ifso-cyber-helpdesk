from app.chatbot.question_models import (
    Question,
    QuestionOption,
)
from app.chatbot.questions import QUESTIONS


QUESTION_REGISTRY: dict[str, Question] = {}

for question_id, data in QUESTIONS.items():

    options = [
        QuestionOption(**option)
        for option in data.get("options", [])
    ]

    QUESTION_REGISTRY[question_id] = Question(
        id=data["id"],
        question=data["question"],
        type=data["type"],
        required=data.get("required", False),
        placeholder=data.get("placeholder"),
        help_text=data.get("help_text"),
        options=options,
        next=data.get("next"),
    )


class QuestionRegistry:

    @staticmethod
    def get(question_id: str) -> Question:

        question = QUESTION_REGISTRY.get(question_id)

        if question is None:
            raise ValueError(f"Unknown question: {question_id}")

        return question