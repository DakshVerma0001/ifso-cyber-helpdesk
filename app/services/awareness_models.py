from pydantic import BaseModel


class AwarenessResponse(BaseModel):

    success: bool

    category: str | None = None

    title: str | None = None

    description: str

    red_flags: list[str]

    recommended_actions: list[str]

    prevention_tips: list[str] = []

    confidence: float = 0.0