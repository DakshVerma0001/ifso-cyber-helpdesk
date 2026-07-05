from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ClassifyRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="Message, SMS, email or chat text to analyze.",
    )


class ClassifyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str

    confidence: float

    category: str | None

    score: int

    red_flags: list[str]

    explanation: str