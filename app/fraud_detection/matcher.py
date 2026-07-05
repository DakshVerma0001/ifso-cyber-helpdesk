from app.fraud_detection.patterns import AMOUNT_PATTERN
from app.fraud_detection.patterns import EMAIL_PATTERN
from app.fraud_detection.patterns import OTP_PATTERN
from app.fraud_detection.patterns import PHONE_PATTERN
from app.fraud_detection.patterns import UPI_PATTERN
from app.fraud_detection.patterns import URL_PATTERN


class PatternMatcher:

    @staticmethod
    def detect(message: str):

        return {
            "urls": URL_PATTERN.findall(message),
            "emails": EMAIL_PATTERN.findall(message),
            "phones": PHONE_PATTERN.findall(message),
            "upi_ids": UPI_PATTERN.findall(message),
            "amounts": AMOUNT_PATTERN.findall(message),
            "otp_codes": OTP_PATTERN.findall(message),
        }