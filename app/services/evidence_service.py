from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

from app.fraud_detection.matcher import PatternMatcher
from app.schemas.evidence import EvidenceExtractionResult


class EvidenceService:
    _bank_aliases: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("State Bank of India", ("state bank of india", "sbi")),
        ("HDFC Bank", ("hdfc bank", "hdfc")),
        ("ICICI Bank", ("icici bank", "icici")),
        ("Axis Bank", ("axis bank", "axis")),
        ("Kotak Mahindra Bank", ("kotak mahindra bank", "kotak bank", "kotak")),
        ("Bank of Baroda", ("bank of baroda", "bob")),
        ("Punjab National Bank", ("punjab national bank", "pnb")),
        ("Canara Bank", ("canara bank",)),
        ("Union Bank of India", ("union bank of india", "union bank")),
        ("Bank of India", ("bank of india", "boi")),
        ("Yes Bank", ("yes bank",)),
        ("Indian Bank", ("indian bank",)),
        ("Indian Overseas Bank", ("indian overseas bank",)),
        ("UCO Bank", ("uco bank",)),
        ("Central Bank of India", ("central bank of india",)),
        ("Federal Bank", ("federal bank",)),
        ("IDFC First Bank", ("idfc first bank",)),
        ("Paytm Payments Bank", ("paytm payments bank",)),
    )

    _transaction_patterns: tuple[re.Pattern[str], ...] = (
        re.compile(
            r"\b(?:txn\s*id|txn\s*no|txnid|txn|transaction\s*id|transaction\s*no|transaction\s*number|utr\s*no|utr|rrn|ref(?:erence)?(?:\s*no|\s*number)?|upi\s*ref|imps\s*ref|neft\s*ref|rtgs\s*ref|order\s*id)"
            r"[:#\-\s]*([A-Za-z0-9][A-Za-z0-9\-/_]{5,})\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:trans(?:action)?\s*(?:id|no|number)?|payment\s*id)\s*[:#\-\s]*([A-Za-z0-9][A-Za-z0-9\-/_]{5,})\b",
            re.IGNORECASE,
        ),
    )

    _upi_spaced_pattern = re.compile(
        r"\b([A-Za-z0-9._\-]{2,256})\s*@\s*([A-Za-z0-9]{2,64})\b"
    )

    def extract(
        self,
        messages: str | list[str],
    ) -> EvidenceExtractionResult:
        texts = self._normalize_messages(messages)

        detected = {
            "phone_numbers": [],
            "emails": [],
            "urls": [],
            "upi_ids": [],
            "amounts": [],
            "otp_codes": [],
            "bank_names": [],
            "transaction_ids": [],
        }

        for text in texts:
            patterns = PatternMatcher.detect(text)
            detected["phone_numbers"].extend(patterns.get("phones", []))
            detected["emails"].extend(patterns.get("emails", []))
            detected["urls"].extend(patterns.get("urls", []))
            detected["upi_ids"].extend(patterns.get("upi_ids", []))
            detected["amounts"].extend(patterns.get("amounts", []))
            detected["otp_codes"].extend(patterns.get("otp_codes", []))
            detected["upi_ids"].extend(self._extract_spaced_upi_ids(text))
            detected["transaction_ids"].extend(self._extract_transaction_ids(text))
            detected["bank_names"].extend(self._extract_bank_names(text))

        detected["phone_numbers"] = self._unique_preserve_order(
            detected["phone_numbers"]
        )
        detected["emails"] = self._unique_preserve_order(detected["emails"])
        detected["urls"] = self._unique_preserve_order(detected["urls"])
        detected["upi_ids"] = self._filter_upi_ids(
            self._unique_preserve_order(detected["upi_ids"]),
            texts,
        )
        detected["transaction_ids"] = self._unique_preserve_order(
            detected["transaction_ids"]
        )
        detected["amounts"] = self._filter_amounts(
            self._unique_preserve_order(detected["amounts"]),
            detected["phone_numbers"],
            detected["transaction_ids"],
        )
        detected["otp_codes"] = self._filter_otp_codes(
            self._unique_preserve_order(detected["otp_codes"]),
            texts,
            detected["amounts"],
            detected["phone_numbers"],
            detected["transaction_ids"],
        )
        detected["bank_names"] = self._unique_preserve_order(detected["bank_names"])

        return EvidenceExtractionResult(
            phone_numbers=detected["phone_numbers"],
            emails=detected["emails"],
            urls=detected["urls"],
            upi_ids=detected["upi_ids"],
            amounts=detected["amounts"],
            otp_codes=detected["otp_codes"],
            bank_names=detected["bank_names"],
            transaction_ids=detected["transaction_ids"],
        )

    def _normalize_messages(self, messages: str | list[str]) -> list[str]:
        if isinstance(messages, str):
            return [messages]
        return [message for message in messages if isinstance(message, str) and message.strip()]

    def _extract_spaced_upi_ids(self, text: str) -> list[str]:
        return [
            f"{user}@{provider}"
            for user, provider in self._upi_spaced_pattern.findall(text)
        ]

    def _filter_upi_ids(self, upi_ids: list[str], texts: list[str]) -> list[str]:
        filtered: list[str] = []
        lower_texts = [text.lower() for text in texts]

        for upi_id in upi_ids:
            candidate = upi_id.lower()
            if any(f"{candidate}." in text for text in lower_texts):
                continue
            filtered.append(upi_id)

        return filtered

    def _extract_transaction_ids(self, text: str) -> list[str]:
        found: list[str] = []
        for pattern in self._transaction_patterns:
            found.extend(pattern.findall(text))
        return found

    def _extract_bank_names(self, text: str) -> list[str]:
        normalized_text = self._normalize_text(text)
        tokens = normalized_text.split()
        matches: list[str] = []

        for canonical_name, aliases in self._bank_aliases:
            if any(self._contains_alias(normalized_text, alias) for alias in aliases):
                matches.append(canonical_name)
                continue

            if any(self._fuzzy_match(tokens, alias) for alias in aliases):
                matches.append(canonical_name)

        return matches

    def _filter_amounts(
        self,
        amounts: list[str],
        phone_numbers: list[str],
        transaction_ids: list[str],
    ) -> list[str]:
        blocked = {
            self._strip_non_digits(value)
            for value in phone_numbers + transaction_ids
        }
        amount_context_pattern = re.compile(
            r"(?:₹|rs\.?|inr|rupees?|amount|paid|payment|debit|credited|spent|transfer|loan|cash|refund|balance)",
            re.IGNORECASE,
        )
        filtered: list[str] = []

        for amount in amounts:
            digits = self._strip_non_digits(amount)
            if digits and digits in blocked:
                continue

            if not amount_context_pattern.search(amount):
                if not re.search(r"[₹,\.]", amount):
                    continue

            if digits and len(digits) >= 8 and not amount_context_pattern.search(amount):
                continue

            filtered.append(amount)

        return filtered

    def _filter_otp_codes(
        self,
        otp_codes: list[str],
        texts: list[str],
        amounts: list[str],
        phone_numbers: list[str],
        transaction_ids: list[str],
    ) -> list[str]:
        blocked = {
            self._strip_non_digits(value)
            for value in amounts + phone_numbers + transaction_ids
        }
        context_pattern = re.compile(
            r"(?:otp|one\s*time\s*password|verification\s*code|security\s*code|auth(?:entication)?\s*code|passcode|pin)",
            re.IGNORECASE,
        )

        filtered: list[str] = []
        for otp_code in otp_codes:
            digits = self._strip_non_digits(otp_code)
            if not digits:
                continue

            if digits in blocked and not any(
                context_pattern.search(text) and digits in text for text in texts
            ):
                continue

            if not any(
                context_pattern.search(text) and digits in text for text in texts
            ):
                continue

            filtered.append(otp_code)

        return filtered

    def _contains_alias(self, text: str, alias: str) -> bool:
        normalized_alias = self._normalize_text(alias)
        return normalized_alias in text

    def _fuzzy_match(self, tokens: list[str], alias: str) -> bool:
        alias_tokens = self._normalize_text(alias).split()
        if not alias_tokens:
            return False

        window_size = len(alias_tokens)
        if len(tokens) < window_size:
            candidates = [" ".join(tokens)]
        else:
            candidates = [
                " ".join(tokens[index : index + window_size])
                for index in range(len(tokens) - window_size + 1)
            ]

        normalized_alias = " ".join(alias_tokens)
        for candidate in candidates:
            if SequenceMatcher(None, candidate, normalized_alias).ratio() >= 0.88:
                return True

        return False

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9@.\-\s]", " ", text.lower())).strip()

    def _strip_non_digits(self, value: str) -> str:
        return re.sub(r"\D", "", value)

    def _unique_preserve_order(self, values: list[str]) -> list[str]:
        seen: set[str] = set()
        unique: list[str] = []

        for value in values:
            normalized = value.strip()
            if not normalized:
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(normalized)

        return unique
