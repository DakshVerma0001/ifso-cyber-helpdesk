from pydantic import BaseModel


class AnalyzeRequest(BaseModel):

    message: str


class AnalyzeResponse(BaseModel):

    fraud_type: str

    confidence: float

    source: str

    severity: str

    description: str | None = None

    explanation: list[str] = []

    recommended_actions: list[str] = []