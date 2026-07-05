from pydantic import BaseModel


class FraudAnalysisResult(BaseModel):
    label: str

    confidence: float

    category: str | None = None

    score: int

    red_flags: list[str]

    explanation: str