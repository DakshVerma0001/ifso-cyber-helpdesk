from functools import lru_cache

from app.chatbot.conversation_manager import ConversationManager
from app.chatbot.processor import ConversationProcessor
from app.chatbot.response_models import ConversationResponse
from app.chatbot.session_store import SessionStore
from app.services.fraud_investigation_service import (
    FraudInvestigationService,
)
from app.services.awareness_service import (
    AwarenessService,
)


class ChatbotService:

    def __init__(self):

        self.manager = ConversationManager()

        self.processor = ConversationProcessor()

        self.store = SessionStore()

        self.investigation_service = FraudInvestigationService()

        self.awareness_service = AwarenessService()

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

        if session.mode == "awareness":

            response = self.awareness_service.answer(
                answer
            )

            return ConversationResponse(

                session_id=session.session_id,

                completed=False,

                message=(
                    f"## {response.title}\n\n"
                    f"{response.description}\n\n"
                    f"Recommended Actions:\n"
                    + "\n".join(
                        f"• {item}"
                        for item in response.recommended_actions
                    )
                ),

                fraud_type=response.category,
            )

        question = self.processor.process_answer(
            session,
            answer,
        )

        self.store.update(session)

        # Conversation Finished
        if question is None:

            report = self.investigation_service.investigate(

                description=session.description,

                incident_channel=session.fraud_channel,

                loss_amount=session.amount,
            )

            return ConversationResponse(

                session_id=session.session_id,

                completed=True,

                fraud_type=report.fraud_type,

                confidence=report.confidence,

                severity=report.severity,

                description=report.description,

                red_flags=report.explanation,

                recommended_actions=report.recommended_actions,

                evidence_required=report.evidence_required,

                evidence=report.evidence,

                complaint_ready=False,

                complaint=None,

                message=(
                    "Investigation completed successfully. "
                    "Please upload the required evidence to continue."
                ),
            )

        return ConversationResponse(

            session_id=session.session_id,

            completed=False,

            question=question,

            fraud_type=session.fraud_type,

            complaint_ready=False,
        )


@lru_cache(maxsize=1)
def get_chatbot_service() -> ChatbotService:

    return ChatbotService()