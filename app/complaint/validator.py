from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any


class ComplaintValidator:
    _transaction_id_re = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\-/:._]{5,79}$")
    _upi_id_re = re.compile(r"^[A-Za-z0-9._\-]{2,256}@[A-Za-z0-9]{2,64}$")
    _email_re = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}$"
    )
    _phone_re = re.compile(r"^(?:\+91[\s-]?)?[6-9]\d{9}$")

    @classmethod
    def validate_transaction_ids(cls, transaction_ids: Sequence[str]) -> list[dict[str, Any]]:
        return cls._validate_values(
            transaction_ids,
            field_name="transaction_ids",
            pattern=cls._transaction_id_re,
            error_code="invalid_transaction_id",
            message="Transaction ID must be alphanumeric and at least 6 characters long.",
        )

    @classmethod
    def validate_upi_ids(cls, upi_ids: Sequence[str]) -> list[dict[str, Any]]:
        return cls._validate_values(
            upi_ids,
            field_name="upi_id",
            pattern=cls._upi_id_re,
            error_code="invalid_upi_id",
            message="UPI ID must follow the format name@provider.",
        )

    @classmethod
    def validate_phone_numbers(cls, phone_numbers: Sequence[str]) -> list[dict[str, Any]]:
        return cls._validate_values(
            phone_numbers,
            field_name="phone_number",
            pattern=cls._phone_re,
            error_code="invalid_phone_number",
            message="Phone number must be a valid Indian mobile number.",
        )

    @classmethod
    def validate_email_addresses(cls, email_addresses: Sequence[str]) -> list[dict[str, Any]]:
        return cls._validate_values(
            email_addresses,
            field_name="email_address",
            pattern=cls._email_re,
            error_code="invalid_email_address",
            message="Email address must be valid.",
        )

    @classmethod
    def _validate_values(
        cls,
        values: Sequence[str],
        *,
        field_name: str,
        pattern: re.Pattern[str],
        error_code: str,
        message: str,
    ) -> list[dict[str, Any]]:
        errors: list[dict[str, Any]] = []

        for index, value in enumerate(values):
            candidate = value.strip() if isinstance(value, str) else ""
            if not candidate or pattern.fullmatch(candidate) is None:
                errors.append(
                    {
                        "field": field_name,
                        "index": index,
                        "value": value,
                        "error_code": error_code,
                        "message": message,
                    }
                )

        return errors
