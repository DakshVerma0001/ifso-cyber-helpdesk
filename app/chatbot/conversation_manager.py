from datetime import datetime
from uuid import uuid4

from app.chatbot.conversation_schema import ConversationSession
from app.chatbot.conversation_state import ConversationState
from app.chatbot.question_models import Question
from app.chatbot.state_machine import ConversationStateMachine


class ConversationManager:

    def create_session(self) -> ConversationSession:

        return ConversationSession(
            session_id=str(uuid4()),
            current_state=ConversationState.WELCOME.value,
        )

    def start(self):

        return ConversationStateMachine.get_question(
            ConversationState.WELCOME.value
        )

        return question
    

    def next_question(
        self,
        session: ConversationSession,
        answer: str,
    ) -> Question | None:

        current = ConversationStateMachine.get_question(
            session.current_state
        )

        next_question = ConversationStateMachine.next_question(
            current,
            answer,
        )

        session.updated_at = datetime.utcnow()

        if next_question is not None:
            session.current_state = next_question.id

        return next_question