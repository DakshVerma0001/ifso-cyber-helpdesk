from pydantic import BaseModel, Field


class ClassificationResponse(BaseModel):

    fraud_type: str

    confidence: float

    source: str

    severity: str

    description: str | None = None

    explanation: list[str] = Field(default_factory=list)

    recommended_actions: list[str] = Field(default_factory=list)