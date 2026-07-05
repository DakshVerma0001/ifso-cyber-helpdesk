from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from app.complaint.complaint_templates import ComplaintTemplates
from app.complaint.formatter import ComplaintFormatter
from app.complaint.validator import ComplaintValidator
from app.schemas.complaint import ComplaintData


class ComplaintBuilder:
    def build(self, data: ComplaintData | Mapping[str, Any]) -> dict[str, Any]:
        complaint = self._coerce_model(data)
        raw_data = complaint.model_dump()

        formatted = self._format_complaint(raw_data)
        validation_errors = self._validate_complaint(formatted)

        complaint_dict = ComplaintFormatter.remove_empty_fields(formatted)

        return {
            "complaint": complaint_dict,
            "validation": {
                "is_valid": not validation_errors,
                "errors": validation_errors,
            },
            "templates": {
                "ncrp": ComplaintTemplates.ncrp_complaint(complaint_dict),
                "police": ComplaintTemplates.police_complaint(complaint_dict),
                "bank": ComplaintTemplates.bank_complaint(complaint_dict),
                "internal_investigation": ComplaintTemplates.internal_investigation_report(complaint_dict),
            },
        }

    def _coerce_model(self, data: ComplaintData | Mapping[str, Any]) -> ComplaintData:
        if isinstance(data, ComplaintData):
            return data
        return ComplaintData.model_validate(data)

    def _format_complaint(self, complaint: dict[str, Any]) -> dict[str, Any]:
        formatted = {
            key: ComplaintFormatter.normalize_whitespace(value) if isinstance(value, str) else value
            for key, value in complaint.items()
        }

        formatted["transaction_ids"] = ComplaintFormatter.format_transaction_lists(
            complaint.get("transaction_ids", [])
        )
        formatted["phone_numbers"] = ComplaintFormatter.format_phone_numbers(
            complaint.get("phone_numbers", [])
        )
        formatted["email_addresses"] = [
            email
            for email in (
                ComplaintFormatter.normalize_whitespace(value)
                for value in complaint.get("email_addresses", [])
            )
            if email
        ]
        formatted["social_media_accounts"] = [
            account
            for account in (
                ComplaintFormatter.normalize_whitespace(value)
                for value in complaint.get("social_media_accounts", [])
            )
            if account
        ]
        formatted["evidence"] = ComplaintFormatter.sort_evidence(
            complaint.get("evidence", [])
        )
        formatted["recommended_actions"] = [
            action
            for action in (
                ComplaintFormatter.normalize_whitespace(value)
                for value in complaint.get("recommended_actions", [])
            )
            if action
        ]

        amount_lost = formatted.get("amount_lost")
        if isinstance(amount_lost, Decimal):
            formatted["amount_lost"] = str(amount_lost)

        return formatted

    def _validate_complaint(self, complaint: dict[str, Any]) -> list[dict[str, Any]]:
        errors: list[dict[str, Any]] = []

        transaction_ids = complaint.get("transaction_ids", [])
        if transaction_ids:
            errors.extend(ComplaintValidator.validate_transaction_ids(transaction_ids))

        upi_id = complaint.get("upi_id")
        if upi_id:
            errors.extend(ComplaintValidator.validate_upi_ids([upi_id]))

        victim_phone = complaint.get("victim_phone")
        if victim_phone:
            errors.extend(ComplaintValidator.validate_phone_numbers([victim_phone]))

        phone_numbers = complaint.get("phone_numbers", [])
        if phone_numbers:
            errors.extend(ComplaintValidator.validate_phone_numbers(phone_numbers))

        victim_email = complaint.get("victim_email")
        if victim_email:
            errors.extend(ComplaintValidator.validate_email_addresses([victim_email]))

        email_addresses = complaint.get("email_addresses", [])
        if email_addresses:
            errors.extend(ComplaintValidator.validate_email_addresses(email_addresses))

        return errors
