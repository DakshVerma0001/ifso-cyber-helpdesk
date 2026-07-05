from __future__ import annotations

from pydantic import BaseModel, Field


class FraudRule(BaseModel):

    id: str

    name: str

    weight: int = Field(
        ge=1,
        le=100,
    )

    keywords: list[str] = Field(
        default_factory=list,
    )

    regex: list[str] = Field(
        default_factory=list,
    )

    explanation: str

    confidence: int = Field(
        default=100,
        ge=0,
        le=100,
    )

    examples: list[str] = Field(
        default_factory=list,
    )

    evidence_required: list[str] = Field(
        default_factory=list,
    )


class FraudCategory(BaseModel):

    category: str

    display_name: str

    severity: str

    financial: bool

    description: str

    recommended_actions: list[str] = Field(
        default_factory=list,
    )

    prevention_tips: list[str] = Field(
        default_factory=list,
    )

    rules: list[FraudRule] = Field(
        default_factory=list,
    )