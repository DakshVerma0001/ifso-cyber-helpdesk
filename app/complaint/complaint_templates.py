from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class ComplaintTemplates:
    @staticmethod
    def ncrp_complaint(complaint: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "template_type": "NCRP_COMPLAINT",
            "title": "National Cyber Crime Reporting Portal Complaint",
            "sections": [
                {
                    "name": "Complainant Details",
                    "fields": {
                        "victim_name": complaint.get("victim_name"),
                        "victim_phone": complaint.get("victim_phone"),
                        "victim_email": complaint.get("victim_email"),
                    },
                },
                {
                    "name": "Incident Details",
                    "fields": {
                        "incident_date": complaint.get("incident_date"),
                        "incident_time": complaint.get("incident_time"),
                        "fraud_category": complaint.get("fraud_category"),
                        "incident_description": complaint.get("incident_description"),
                    },
                },
                {
                    "name": "Financial Details",
                    "fields": {
                        "financial_loss": complaint.get("financial_loss"),
                        "amount_lost": complaint.get("amount_lost"),
                        "bank_name": complaint.get("bank_name"),
                        "upi_id": complaint.get("upi_id"),
                        "transaction_ids": complaint.get("transaction_ids", []),
                    },
                },
                {
                    "name": "Supporting Evidence",
                    "fields": {
                        "evidence": complaint.get("evidence", []),
                    },
                },
            ],
        }

    @staticmethod
    def police_complaint(complaint: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "template_type": "POLICE_COMPLAINT",
            "title": "Police Complaint",
            "sections": [
                {
                    "name": "Applicant Details",
                    "fields": {
                        "victim_name": complaint.get("victim_name"),
                        "victim_phone": complaint.get("victim_phone"),
                        "victim_email": complaint.get("victim_email"),
                    },
                },
                {
                    "name": "Incident Summary",
                    "fields": {
                        "incident_date": complaint.get("incident_date"),
                        "incident_time": complaint.get("incident_time"),
                        "fraud_category": complaint.get("fraud_category"),
                        "incident_description": complaint.get("incident_description"),
                    },
                },
                {
                    "name": "Identifiers",
                    "fields": {
                        "phone_numbers": complaint.get("phone_numbers", []),
                        "email_addresses": complaint.get("email_addresses", []),
                        "social_media_accounts": complaint.get("social_media_accounts", []),
                        "website_url": complaint.get("website_url"),
                    },
                },
                {
                    "name": "Evidence",
                    "fields": {
                        "evidence": complaint.get("evidence", []),
                    },
                },
            ],
        }

    @staticmethod
    def bank_complaint(complaint: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "template_type": "BANK_COMPLAINT",
            "title": "Bank Complaint",
            "sections": [
                {
                    "name": "Customer Details",
                    "fields": {
                        "victim_name": complaint.get("victim_name"),
                        "victim_phone": complaint.get("victim_phone"),
                        "victim_email": complaint.get("victim_email"),
                        "bank_name": complaint.get("bank_name"),
                    },
                },
                {
                    "name": "Transaction Details",
                    "fields": {
                        "financial_loss": complaint.get("financial_loss"),
                        "amount_lost": complaint.get("amount_lost"),
                        "transaction_ids": complaint.get("transaction_ids", []),
                        "upi_id": complaint.get("upi_id"),
                    },
                },
                {
                    "name": "Incident Details",
                    "fields": {
                        "incident_date": complaint.get("incident_date"),
                        "incident_time": complaint.get("incident_time"),
                        "incident_description": complaint.get("incident_description"),
                    },
                },
            ],
        }

    @staticmethod
    def internal_investigation_report(complaint: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "template_type": "INTERNAL_INVESTIGATION_REPORT",
            "title": "Internal Investigation Report",
            "sections": [
                {
                    "name": "Case Summary",
                    "fields": {
                        "fraud_category": complaint.get("fraud_category"),
                        "incident_description": complaint.get("incident_description"),
                        "financial_loss": complaint.get("financial_loss"),
                        "amount_lost": complaint.get("amount_lost"),
                    },
                },
                {
                    "name": "Observed Indicators",
                    "fields": {
                        "transaction_ids": complaint.get("transaction_ids", []),
                        "phone_numbers": complaint.get("phone_numbers", []),
                        "email_addresses": complaint.get("email_addresses", []),
                        "social_media_accounts": complaint.get("social_media_accounts", []),
                    },
                },
                {
                    "name": "Evidence",
                    "fields": {
                        "evidence": complaint.get("evidence", []),
                    },
                },
                {
                    "name": "Recommended Actions",
                    "fields": {
                        "recommended_actions": complaint.get("recommended_actions", []),
                    },
                },
            ],
        }
