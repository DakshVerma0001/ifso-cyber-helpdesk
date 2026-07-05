from __future__ import annotations

from app.chatbot.immediate_actions import IMMEDIATE_ACTIONS
from app.chatbot.investigation_flow import INVESTIGATION_FLOWS
from app.chatbot.question_models import Question
from app.chatbot.question_registry import QUESTION_REGISTRY
from app.chatbot.response_models import ConversationResponse


class InvestigationOrchestrator:

    def next_step(
        self,
        session,
        next_question: Question | None,
    ) -> ConversationResponse:

        if next_question is None:

            return ConversationResponse(
                session_id=session.session_id,
                completed=True,
                message="Investigation completed.",
                fraud_type=session.fraud_type,
                complaint_ready=True,
            )

        actions = self._get_immediate_actions(session)

        return ConversationResponse(
            session_id=session.session_id,
            completed=False,
            question=next_question,
            fraud_type=session.fraud_type,
            immediate_actions=actions,
        )

    def _get_immediate_actions(
        self,
        session,
    ) -> list[str]:

        if session.transaction_time is None:
            return []

        return IMMEDIATE_ACTIONS.get(
            session.transaction_time,
            [],
        )