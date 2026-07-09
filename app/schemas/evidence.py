from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvidenceExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[str] = Field(default_factory=list)


class EvidenceExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_numbers: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    upi_ids: list[str] = Field(default_factory=list)
    amounts: list[str] = Field(default_factory=list)
    otp_codes: list[str] = Field(default_factory=list)
    bank_names: list[str] = Field(default_factory=list)
    transaction_ids: list[str] = Field(default_factory=list)

