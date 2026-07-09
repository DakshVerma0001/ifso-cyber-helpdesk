from app.ml.bert.predictor import BertPredictor

predictor = BertPredictor()

samples = [

    "I received a call asking me to share my OTP.",

    "I scanned a QR code and lost ₹15000.",

    "Someone promised me guaranteed stock returns.",

]

for text in samples:

    print()

    print(text)

    print(predictor.predict(text))