from __future__ import annotations

import os

from reportlab.platypus import (
    SimpleDocTemplate,
)

from app.reports.sections import (
    add_actions,
    add_evidence,
    add_footer,
    add_header,
    add_red_flags,
    add_summary,
)
from app.reports.watermark import draw_watermark
from app.services.investigation_models import InvestigationReport


class PDFGenerator:

    def __init__(self):

        self.logo = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "ifso_logo.png",
        )

    def generate(
        self,
        report: InvestigationReport,
        output_path: str,
    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True,
        )

        story = []

        add_header(
            story,
            report,
            self.logo,
        )

        add_summary(
            story,
            report,
        )

        add_red_flags(
            story,
            report,
        )

        add_evidence(
            story,
            report,
        )

        add_actions(
            story,
            report,
        )

        add_footer(
            story,
        )

        document = SimpleDocTemplate(

            output_path,

            title="IFSO AI Cyber Fraud Investigation Report",

            author="IFSO AI Investigation Engine",

            subject="Cyber Fraud Investigation",

            creator="IFSO",

        )

        document.build(

            story,

            onFirstPage=draw_watermark,

            onLaterPages=draw_watermark,

        )

        return output_path