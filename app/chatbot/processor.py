from datetime import datetime

from app.chatbot.conversation_manager import ConversationManager
from app.chatbot.conversation_schema import ConversationSession
from app.chatbot.state_machine import ConversationStateMachine
from app.chatbot.validators import ConversationValidator
from app.services.classification_service import ClassificationService


class ConversationProcessor:
    def __init__(self) -> None:
        self.manager = ConversationManager()
        self.classifier = ClassificationService()

    def process_answer(
        self,
        session: ConversationSession,
        answer: str,
    ):
        current_question = ConversationStateMachine.get_question(
            session.current_state
        )

        is_valid, error_message = ConversationValidator.validate(
            current_question,
            answer,
        )

        if not is_valid:
            raise ValueError(error_message)

        session.answers[current_question.id] = answer
        session.updated_at = datetime.utcnow()

        self._update_session(session, current_question.id, answer)

        next_question = self.manager.next_question(
            session=session,
            answer=answer,
        )

        return next_question

    def _update_session(
        self,
        session: ConversationSession,
        question_id: str,
        answer: str,
    ) -> None:

        match question_id:

            case "AMOUNT":
                session.amount = float(answer)

            case "FRAUD_CHANNEL":
                session.fraud_channel = answer

            case "INCIDENT_TIME":
                session.transaction_time = answer

            case "MESSAGE_INPUT":
                result = self.classifier.classify(answer)

                session.fraud_type = result.fraud_type

                session.answers["MESSAGE_ANALYSIS"] = result.model_dump()

            case "DESCRIPTION":
                session.description = answer

                result = self.classifier.classify(answer)

                session.fraud_type = result.fraud_type

                session.answers["CLASSIFICATION"] = result.model_dump()

            case _:
                pass