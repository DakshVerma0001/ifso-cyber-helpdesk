from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TimelineAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime | None = None
    question: str | None = None
    answer: str = Field(default="")
    source: str | None = None
    order: int | None = None


class TimelineBuildRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answers: list[TimelineAnswer] = Field(default_factory=list)


class TimelineEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: str | None = None
    event: str
    source: str | None = None
    order: int

