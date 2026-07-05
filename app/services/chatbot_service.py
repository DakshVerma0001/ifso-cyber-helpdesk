from functools import lru_cache

from app.chatbot.conversation_manager import ConversationManager
from app.chatbot.processor import ConversationProcessor
from app.chatbot.response_models import ConversationResponse
from app.chatbot.session_store import SessionStore


class ChatbotService:

    def __init__(self):

        self.manager = ConversationManager()

        self.processor = ConversationProcessor()

        self.store = SessionStore()

    def start(self) -> ConversationResponse:

        session = self.manager.create_session()

        self.store.create(session)

        return ConversationResponse(
            session_id=session.session_id,
            question=self.manager.start(),
        )

    def reply(
        self,
        session_id: str,
        answer: str,
    ) -> ConversationResponse:

        session = self.store.get(session_id)

        if session is None:

            raise ValueError("Invalid session.")

        question = self.processor.process_answer(
            session,
            answer,
        )

        self.store.update(session)

        return ConversationResponse(
            session_id=session.session_id,
            question=question,
            fraud_type=session.fraud_type,
        )


@lru_cache(maxsize=1)
def get_chatbot_service() -> ChatbotService:
    return ChatbotService()