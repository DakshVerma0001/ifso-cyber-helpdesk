from app.chatbot.question_models import Question
from app.chatbot.question_registry import QUESTION_REGISTRY


class ConversationStateMachine:
    @staticmethod
    def get_question(question_id: str) -> Question:

        if question_id not in QUESTION_REGISTRY:
            raise ValueError(f"Unknown question: {question_id}")

        return QUESTION_REGISTRY[question_id]

    @staticmethod
    def next_question(
        current_question: Question,
        answer: str | None,
    ) -> Question | None:

        if current_question.next is None:
            return None

        if isinstance(current_question.next, str):
            return ConversationStateMachine.get_question(
                current_question.next
            )

        next_question_id = current_question.next.get(answer)

        if next_question_id is None:
            raise ValueError(
                f"No transition defined for answer '{answer}' "
                f"from question '{current_question.id}'"
            )

        return ConversationStateMachine.get_question(
            next_question_id
        )