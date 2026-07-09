from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class UploadedEvidence(BaseModel):

    evidence_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    evidence_type: str

    filename: str

    file_path: str

    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class EvidenceCollection(BaseModel):

    required: list[str] = Field(
        default_factory=list
    )

    uploaded: list[UploadedEvidence] = Field(
        default_factory=list
    )

    missing: list[str] = Field(
        default_factory=list
    )

    completed: bool = False