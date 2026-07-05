from __future__ import annotations

import re

from app.chatbot.question_models import Question, QuestionType


class ConversationValidator:

    @staticmethod
    def validate(
        question: Question,
        answer: str,
    ) -> tuple[bool, str | None]:

        if question.required and not answer.strip():
            return False, "This field is required."

        if question.type == QuestionType.NUMBER:

            try:
                value = float(answer)

                if value < 0:
                    return False, "Amount cannot be negative."

            except ValueError:
                return False, "Please enter a valid amount."

        elif question.type == QuestionType.SINGLE_SELECT:

            valid_options = {
                option.id
                for option in question.options
            }

            if answer not in valid_options:
                return (
                    False,
                    "Invalid option selected.",
                )

        elif question.type == QuestionType.TEXT:

            if len(answer.strip()) < 3:
                return (
                    False,
                    "Please provide more information.",
                )

        return True, None