from __future__ import annotations

from collections.abc import Mapping, Sequence
import re
from typing import Any


class ComplaintFormatter:
    _whitespace_re = re.compile(r"\s+")

    @classmethod
    def normalize_whitespace(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = cls._whitespace_re.sub(" ", value).strip()
        return normalized or None

    @classmethod
    def remove_empty_fields(cls, data: Mapping[str, Any]) -> dict[str, Any]:
        cleaned: dict[str, Any] = {}

        for key, value in data.items():
            normalized = cls._clean_value(value)
            if normalized is not None:
                cleaned[key] = normalized

        return cleaned

    @classmethod
    def sort_evidence(cls, evidence: Sequence[str]) -> list[str]:
        return sorted(
            {
                item
                for item in (
                    cls.normalize_whitespace(value)
                    for value in evidence
                )
                if item
            },
            key=str.lower,
        )

    @classmethod
    def format_transaction_lists(cls, transaction_ids: Sequence[str]) -> list[str]:
        return [
            transaction
            for transaction in (
                cls.normalize_whitespace(value)
                for value in transaction_ids
            )
            if transaction
        ]

    @classmethod
    def format_phone_numbers(cls, phone_numbers: Sequence[str]) -> list[str]:
        normalized_numbers = []

        for phone in phone_numbers:
            normalized = cls.normalize_whitespace(phone)
            if normalized:
                normalized_numbers.append(normalized)

        return normalized_numbers

    @classmethod
    def _clean_value(cls, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, str):
            return cls.normalize_whitespace(value)

        if isinstance(value, Mapping):
            nested = cls.remove_empty_fields(value)
            return nested or None

        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            cleaned_items = [
                item
                for item in (cls._clean_value(item) for item in value)
                if item is not None and item != []
            ]
            return cleaned_items or None

        return value
