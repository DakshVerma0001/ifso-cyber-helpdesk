from app.fraud_detection.rule_engine import RuleEngine

engine = RuleEngine()

messages = [
    "I received a phone call asking me to share my OTP.",
    "I scanned a QR code and lost ₹15000.",
    "Someone promised me guaranteed stock returns."
]

for message in messages:
    print("=" * 80)
    print(message)
    result = engine.analyze(message)
    print(result)