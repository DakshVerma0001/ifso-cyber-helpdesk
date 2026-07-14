from __future__ import annotations

from app.knowledge.awareness_manager import AwarenessManager
from app.knowledge.manager import KnowledgeManager
from app.services.awareness_models import AwarenessResponse
from app.services.classification_service import ClassificationService


class AwarenessService:

    def __init__(self):

        self.awareness = AwarenessManager()

        self.classifier = ClassificationService()

        self.knowledge = KnowledgeManager()

    def _detect_intent(
        self,
        question: str,
    ) -> str:

        question = question.lower().strip()

        awareness_patterns = [

            "how do i",
            "how can i",
            "how should i",
            "how to",

            "report",
            "complaint",
            "file complaint",

            "helpline",
            "1930",

            "prevent",
            "prevention",

            "protect",

            "stay safe",

            "guidelines",

            "tips",

            "best practices",

            "where do i report",

            "where can i report",

            "safe online",

            "security",

            "precautions",

            "avoid scam",

            "avoid fraud",

            "cyber hygiene",

            "online banking safety",

            "password safety",

            "otp safety",
        ]

        fraud_patterns = [

            "what is",

            "what's",

            "explain",

            "meaning",

            "define",

            "how does",

            "types of",

            "digital arrest",

            "otp fraud",

            "phishing",

            "smishing",

            "vishing",

            "upi fraud",

            "investment fraud",

            "loan fraud",

            "remote access",

            "qr scam",

            "courier scam",

            "parcel scam",
        ]

        for pattern in awareness_patterns:

            if pattern in question:

                return "awareness"

        for pattern in fraud_patterns:

            if pattern in question:

                return "fraud"

        return "unknown"

    def answer(
        self,
        question: str,
    ) -> AwarenessResponse:

        intent = self._detect_intent(
            question
        )

        # ------------------------------------------
        # Awareness Mode
        # ------------------------------------------

        if intent == "awareness":

            awareness = self.awareness.find(
                question
            )

            if awareness is not None:

                actions = []

                actions.extend(
                    awareness.get(
                        "guidelines",
                        []
                    )
                )

                actions.extend(
                    awareness.get(
                        "do",
                        []
                    )
                )

                for contact in awareness.get(
                    "emergency_contacts",
                    []
                ):

                    actions.append(
                        f"{contact['name']}: {contact['value']}"
                    )

                for resource in awareness.get(
                    "official_resources",
                    []
                ):

                    actions.append(
                        f"{resource['title']}: {resource['url']}"
                    )

                return AwarenessResponse(

                    success=True,

                    category=awareness.get(
                        "topic"
                    ),

                    title=awareness.get(
                        "display_name"
                    ),

                    description=awareness.get(
                        "description",
                        ""
                    ),

                    red_flags=[],

                    recommended_actions=actions,

                    prevention_tips=awareness.get(
                        "dont",
                        []
                    ),

                    confidence=1.0,
                )

            return AwarenessResponse(

                success=False,

                title="Cyber Fraud Awareness Assistant",

                description=(
                    "I couldn't find a suitable awareness guide "
                    "for your query."
                ),

                red_flags=[],

                recommended_actions=[
                    "Please rephrase your question."
                ],

                prevention_tips=[],

                confidence=1.0,
            )

        # ------------------------------------------
        # Fraud Mode
        # ------------------------------------------

        if intent == "fraud":

            classification = self.classifier.classify(
                question
            )

            if classification.confidence < 0.65:

                return AwarenessResponse(

                    success=False,

                    title="Cyber Fraud Awareness Assistant",

                    description=(
                        "I couldn't confidently identify the cyber fraud "
                        "topic you're asking about. Please rephrase your "
                        "question or ask about a specific cyber fraud."
                    ),

                    red_flags=[],

                    recommended_actions=[
                        "Ask about phishing scams.",
                        "Ask about OTP fraud.",
                        "Ask about UPI fraud.",
                        "Ask about digital arrest.",
                        "Ask about investment scams.",
                    ],

                    prevention_tips=[],

                    confidence=classification.confidence,
                )

            knowledge = self._get_category(
                classification.fraud_type
            )

            if knowledge is None:

                return AwarenessResponse(

                    success=False,

                    title="Cyber Fraud Awareness Assistant",

                    description=(
                        "Sorry, I couldn't find sufficient information "
                        "about that cyber fraud."
                    ),

                    red_flags=[],

                    recommended_actions=[
                        "Please ask another cyber fraud related question."
                    ],

                    prevention_tips=[],

                    confidence=classification.confidence,
                )

            red_flags = []

            for rule in knowledge.get(
                "rules",
                [],
            ):

                explanation = rule.get(
                    "explanation"
                )

                if explanation:

                    red_flags.append(
                        explanation
                    )

            return AwarenessResponse(

                success=True,

                category=knowledge.get(
                    "category"
                ),

                title=knowledge.get(
                    "display_name"
                ),

                description=knowledge.get(
                    "description",
                    ""
                ),

                red_flags=red_flags,

                recommended_actions=knowledge.get(
                    "recommended_actions",
                    []
                ),

                prevention_tips=[],

                confidence=classification.confidence,
            )

        # ------------------------------------------
        # Unknown Intent
        # ------------------------------------------

        return AwarenessResponse(

            success=False,

            title="Cyber Fraud Awareness Assistant",

            description=(
                "I am here to help only with cyber fraud related questions "
                "and awareness. Please ask about phishing, UPI fraud, OTP "
                "fraud, digital arrest, online banking safety, cyber crime "
                "reporting or other cyber security scams."
            ),

            red_flags=[],

            recommended_actions=[
                "What is digital arrest?",
                "Explain phishing.",
                "How do I report cyber fraud?",
                "How can I protect my bank account?",
                "How do I stay safe online?",
            ],

            prevention_tips=[],

            confidence=1.0,
        )

    def _get_category(
        self,
        category: str,
    ):

        for item in self.knowledge.get_categories():

            if item.category == category:

                return item.model_dump()

        return None    