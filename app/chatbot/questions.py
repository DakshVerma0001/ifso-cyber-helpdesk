QUESTIONS = {
    "WELCOME": {
        "id": "WELCOME",
        "question": "Hello, I am the IFSO AI Cyber Fraud Investigation Assistant. I will help you understand the fraud, collect the required information and guide you with the next steps.",
        "type": "message",
        "required": False,
        "next": "MONEY_LOST"
    },

    "MONEY_LOST": {
        "id": "MONEY_LOST",
        "question": "Have you already lost money?",
        "type": "single_select",
        "required": True,
        "options": [
            {"id": "YES", "label": "Yes"},
            {"id": "NO", "label": "No"},
            {"id": "NOT_SURE", "label": "Not Sure"}
        ],
        "next": {
            "YES": "AMOUNT",
            "NO": "MESSAGE_AVAILABLE",
            "NOT_SURE": "DESCRIPTION"
        }
    },

    "AMOUNT": {
        "id": "AMOUNT",
        "question": "Approximately how much money did you lose?",
        "type": "number",
        "required": True,
        "next": "FRAUD_CHANNEL"
    },

    "MESSAGE_AVAILABLE": {
        "id": "MESSAGE_AVAILABLE",
        "question": "Do you have the suspicious message, email, website link or screenshot available for analysis?",
        "type": "single_select",
        "required": True,
        "options": [
            {"id": "YES", "label": "Yes"},
            {"id": "NO", "label": "No"}
        ],
        "next": {
            "YES": "MESSAGE_INPUT",
            "NO": "FRAUD_CHANNEL"
        }
    },

    "MESSAGE_INPUT": {
        "id": "MESSAGE_INPUT",
        "question": "Please paste the suspicious message or describe it.",
        "type": "text",
        "required": True,
        "next": "FRAUD_CHANNEL"
    },

    "FRAUD_CHANNEL": {
        "id": "FRAUD_CHANNEL",
        "question": "How did the fraud happen?",
        "type": "single_select",
        "required": True,
        "options": [
            {"id": "UPI", "label": "UPI"},
            {"id": "BANK_TRANSFER", "label": "Bank Transfer"},
            {"id": "PHONE_CALL", "label": "Phone Call"},
            {"id": "SMS", "label": "SMS"},
            {"id": "EMAIL", "label": "Email"},
            {"id": "WHATSAPP", "label": "WhatsApp"},
            {"id": "SOCIAL_MEDIA", "label": "Social Media"},
            {"id": "WEBSITE", "label": "Website"},
            {"id": "OTHER", "label": "Other"}
        ],
        "next": "INCIDENT_TIME"
    },

    "INCIDENT_TIME": {
        "id": "INCIDENT_TIME",
        "question": "When did the incident occur?",
        "type": "single_select",
        "required": True,
        "options": [
            {"id": "LESS_THAN_1_HOUR", "label": "Within the last hour"},
            {"id": "TODAY", "label": "Today"},
            {"id": "YESTERDAY", "label": "Yesterday"},
            {"id": "OLDER", "label": "Earlier"}
        ],
        "next": "DESCRIPTION"
    },

    "DESCRIPTION": {
        "id": "DESCRIPTION",
        "question": "Please describe what happened in your own words.",
        "type": "text",
        "required": True,
        "next": "CLASSIFICATION"
    }
}

QUESTIONS.update({

    "UPI_APP": {
        "id": "UPI_APP",
        "question": "Which UPI application was used?",
        "type": "single_select",
        "required": True,
        "options": [
            {"id":"PHONEPE","label":"PhonePe"},
            {"id":"GPAY","label":"Google Pay"},
            {"id":"PAYTM","label":"Paytm"},
            {"id":"BHIM","label":"BHIM"},
            {"id":"OTHER","label":"Other"}
        ]
    },

    "UPI_ID": {
        "id":"UPI_ID",
        "question":"Please enter the UPI ID involved.",
        "type":"text",
        "required":True
    },

    "TRANSACTION_ID": {
        "id":"TRANSACTION_ID",
        "question":"Please enter the transaction ID.",
        "type":"text",
        "required":False
    },

    "BANK_NAME":{
        "id":"BANK_NAME",
        "question":"Which bank account was involved?",
        "type":"text",
        "required":True
    },

    "ACCOUNT_NUMBER":{
        "id":"ACCOUNT_NUMBER",
        "question":"Enter the last four digits of the account number.",
        "type":"text",
        "required":False
    },

    "PHONE_NUMBER":{
        "id":"PHONE_NUMBER",
        "question":"Enter the phone number involved.",
        "type":"text",
        "required":False
    },

    "CALL_RECORDING":{
        "id":"CALL_RECORDING",
        "question":"Do you have a call recording?",
        "type":"single_select",
        "options":[
            {"id":"YES","label":"Yes"},
            {"id":"NO","label":"No"}
        ]
    },

    "SCREENSHOTS":{
        "id":"SCREENSHOTS",
        "question":"Do you have screenshots?",
        "type":"single_select",
        "options":[
            {"id":"YES","label":"Yes"},
            {"id":"NO","label":"No"}
        ]
    },

    "EMAIL_ADDRESS":{
        "id":"EMAIL_ADDRESS",
        "question":"Enter the sender's email address.",
        "type":"text"
    },

    "WEBSITE_URL":{
        "id":"WEBSITE_URL",
        "question":"Enter the suspicious website URL.",
        "type":"text"
    },

    "PLATFORM":{
        "id":"PLATFORM",
        "question":"Which social media platform?",
        "type":"single_select",
        "options":[
            {"id":"FACEBOOK","label":"Facebook"},
            {"id":"INSTAGRAM","label":"Instagram"},
            {"id":"X","label":"X"},
            {"id":"TELEGRAM","label":"Telegram"},
            {"id":"OTHER","label":"Other"}
        ]
    },

    "PROFILE_LINK":{
        "id":"PROFILE_LINK",
        "question":"Paste the profile link if available.",
        "type":"text"
    }

})