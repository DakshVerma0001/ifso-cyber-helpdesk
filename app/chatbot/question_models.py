from enum import Enum

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    MESSAGE = "message"

    TEXT = "text"

    NUMBER = "number"

    SINGLE_SELECT = "single_select"

    MULTI_SELECT = "multi_select"


class QuestionOption(BaseModel):

    id: str

    label: str


class Question(BaseModel):

    id: str

    question: str

    type: QuestionType

    required: bool = True

    placeholder: str | None = None

    help_text: str | None = None

    options: list[QuestionOption] = Field(
        default_factory=list
    )

    next: str | dict[str, str] | None = None