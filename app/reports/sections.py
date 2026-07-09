from __future__ import annotations

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.reports.styles import (
    TITLE,
    SECTION,
    NORMAL,
)

from app.reports.qr_generator import QRGenerator


def add_header(
    story,
    report,
    logo_path: str,
):

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=2.8 * cm,
            height=2.8 * cm,
        )

        logo.hAlign = "CENTER"

        story.append(logo)

    story.append(
        Paragraph(
            "<b>INTELLIGENCE FUSION & STRATEGIC OPERATIONS (IFSO)</b>",
            TITLE,
        )
    )

    story.append(
        Paragraph(
            "<b>DELHI POLICE</b>",
            TITLE,
        )
    )

    story.append(
        Paragraph(
            "<b>AI CYBER FRAUD INVESTIGATION REPORT</b>",
            TITLE,
        )
    )

    story.append(
        Paragraph(
            "<font color='red'><b>CONFIDENTIAL - OFFICIAL USE ONLY</b></font>",
            NORMAL,
        )
    )

    story.append(
        Spacer(
            1,
            0.4 * cm,
        )
    )

    qr = QRGenerator.generate(

        report.complaint.complaint_id,

        "generated_reports/qr",
    )

    qr_image = Image(

        qr,

        width=2.8 * cm,

        height=2.8 * cm,
    )

    details = [

        [
            Paragraph("<b>Report ID</b>", NORMAL),
            report.complaint.complaint_id,
            qr_image,
        ],

        [
            Paragraph("<b>Generated</b>", NORMAL),
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            "",
        ],

        [
            Paragraph("<b>Status</b>", NORMAL),
            report.complaint.status,
            "",
        ],

        [
            Paragraph("<b>Fraud Type</b>", NORMAL),
            report.fraud_type,
            "",
        ],

        [
            Paragraph("<b>Severity</b>", NORMAL),
            report.severity,
            "",
        ],

        [
            Paragraph("<b>Confidence</b>", NORMAL),
            f"{report.confidence*100:.2f}%",
            "",
        ],
    ]

    table = Table(

        details,

        colWidths=[
            4 * cm,
            9 * cm,
            3 * cm,
        ],
    )

    table.setStyle(

        TableStyle(

            [

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#003366")),

                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ]

        )

    )

    story.append(table)

    story.append(
        Spacer(
            1,
            0.6 * cm,
        )
    )

def add_summary(
    story,
    report,
):

    story.append(
        Paragraph(
            "INVESTIGATION SUMMARY",
            SECTION,
        )
    )

    summary = f"""
    Based on the victim's statement and hybrid AI analysis,
    this incident has been classified as
    <b>{report.fraud_type}</b> with
    <b>{report.confidence*100:.1f}% confidence</b>.

    The overall risk level has been assessed as
    <b>{report.severity}</b>.

    {report.description}
    """

    story.append(
        Paragraph(
            summary,
            NORMAL,
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )


def add_red_flags(
    story,
    report,
):

    story.append(
        Paragraph(
            "AI DETECTED RED FLAGS",
            SECTION,
        )
    )

    for flag in report.explanation:

        story.append(
            Paragraph(
                f"• {flag}",
                NORMAL,
            )
        )

    story.append(
        Spacer(
            1,
            0.4 * cm,
        )
    )
def add_evidence(
    story,
    report,
):

    story.append(
        Paragraph(
            "EXTRACTED DIGITAL EVIDENCE",
            SECTION,
        )
    )

    entities = report.complaint.entities

    data = [

        ["Evidence", "Value"],

        ["Phone Numbers", ", ".join(entities.phone_numbers) or "-"],

        ["UPI IDs", ", ".join(entities.upi_ids) or "-"],

        ["Emails", ", ".join(entities.emails) or "-"],

        ["URLs", ", ".join(entities.urls) or "-"],

        ["Transaction IDs", ", ".join(entities.transaction_ids) or "-"],

        ["Bank Names", ", ".join(entities.bank_names) or "-"],

        ["Amount Lost", f"₹ {report.complaint.loss_amount or '-'}"],
    ]

    table = Table(
        data,
        colWidths=[5 * cm, 11 * cm],
    )

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ]

        )

    )

    story.append(table)

    story.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )
def add_actions(
    story,
    report,
):

    story.append(
        Paragraph(
            "IMMEDIATE RECOMMENDED ACTIONS",
            SECTION,
        )
    )

    for i, action in enumerate(
        report.recommended_actions,
        start=1,
    ):

        story.append(
            Paragraph(
                f"{i}. {action}",
                NORMAL,
            )
        )

    story.append(
        Spacer(
            1,
            0.4 * cm,
        )
    )

    story.append(
        Paragraph(
            "REQUIRED DIGITAL EVIDENCE",
            SECTION,
        )
    )

    for i, item in enumerate(
        report.evidence_required,
        start=1,
    ):

        story.append(
            Paragraph(
                f"{i}. {item}",
                NORMAL,
            )
        )

    story.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )
def add_footer(
    story,
):

    story.append(
        Paragraph(
            "DISCLAIMER",
            SECTION,
        )
    )

    story.append(
        Paragraph(
            """
            This report has been automatically generated by the
            <b>IFSO AI Cyber Fraud Investigation Engine</b>.

            The findings are intended to assist investigators by
            providing AI-assisted fraud classification, digital
            evidence extraction and investigation recommendations.

            Final legal conclusions and prosecution decisions must
            always be made by an authorised Investigating Officer.
            """,
            NORMAL,
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm,
        )
    )

    story.append(
        Paragraph(
            "<b>Generated by Intelligence Fusion & Strategic Operations (IFSO), Delhi Police</b>",
            NORMAL,
        )
    )