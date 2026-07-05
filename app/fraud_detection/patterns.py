import re

URL_PATTERN = re.compile(
    r"https?://[^\s]+|www\.[^\s]+",
    re.IGNORECASE,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?:\+91[- ]?)?[6-9]\d{9}"
)

OTP_PATTERN = re.compile(
    r"\b\d{4,8}\b"
)

UPI_PATTERN = re.compile(
    r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"
)

AMOUNT_PATTERN = re.compile(
    r"(?:₹|rs\.?|inr)?\s?\d{2,}(?:,\d{3})*(?:\.\d{2})?",
    re.IGNORECASE,
)