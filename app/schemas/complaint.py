from __future__ import annotations

from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ComplaintData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    victim_name: str | None = Field(default=None, min_length=1)
    victim_phone: str | None = Field(default=None, min_length=1)
    victim_email: str | None = Field(default=None, min_length=1)
    incident_date: date | None = None
    incident_time: time | None = None
    incident_description: str | None = Field(default=None, min_length=1)
    fraud_category: str | None = Field(default=None, min_length=1)
    financial_loss: bool = False
    amount_lost: Decimal | None = Field(default=None, ge=0)
    transaction_ids: list[str] = Field(default_factory=list)
    bank_name: str | None = Field(default=None, min_length=1)
    upi_id: str | None = Field(default=None, min_length=1)
    website_url: str | None = Field(default=None, min_length=1)
    phone_numbers: list[str] = Field(default_factory=list)
    email_addresses: list[str] = Field(default_factory=list)
    social_media_accounts: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
