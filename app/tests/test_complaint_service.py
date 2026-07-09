from app.services.complaint_service import ComplaintService

service = ComplaintService()

complaint = service.generate(

    description=(
        "I received a phone call asking me to "
        "share my OTP and lost ₹25000."
    ),

    incident_channel="Phone Call",

    evidence={
        "phone_numbers": [
            "9876543210"
        ],

        "amounts": [
            25000
        ],

        "upi_ids": [
            "fraud@upi"
        ],
    },
)

print()

print(complaint.model_dump_json(indent=2))