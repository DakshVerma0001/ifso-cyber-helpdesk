from __future__ import annotations

from app.chatbot.conversation_schema import ConversationSession


class SessionStore:

    _sessions: dict[str, ConversationSession] = {}

    def create(
        self,
        session: ConversationSession,
    ) -> None:

        self._sessions[session.session_id] = session

    def get(
        self,
        session_id: str,
    ) -> ConversationSession | None:

        return self._sessions.get(session_id)

    def update(
        self,
        session: ConversationSession,
    ) -> None:

        self._sessions[session.session_id] = session

    def exists(
        self,
        session_id: str,
    ) -> bool:

        return session_id in self._sessions