from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

from fastapi import HTTPException

from app.reports.pdf_generator import PDFGenerator
from app.services.fraud_investigation_service import (
    FraudInvestigationService,
)

router = APIRouter(
    prefix="/report",
    tags=["Investigation Report"],
)


@router.post("/generate")
def generate_report(

    description: str,

    incident_channel: str | None = None,

    loss_amount: float | None = None,
):

    report = FraudInvestigationService().investigate(

        description=description,

        incident_channel=incident_channel,

        loss_amount=loss_amount,
    )

    Path("generated_reports").mkdir(
        exist_ok=True
    )

    output = (
        Path("generated_reports")
        / f"{report.complaint.complaint_id}.pdf"
    )

    PDFGenerator().generate(

        report,

        str(output),
    )

    return {

        "success": True,

        "message": "Investigation report generated successfully.",

        "complaint_id": report.complaint.complaint_id,

        "download_url": (
            f"/report/download/"
            f"{report.complaint.complaint_id}"
        ),

        "fraud_type": report.fraud_type,

        "severity": report.severity,

        "confidence": report.confidence,
    }
@router.get("/download/{complaint_id}")
def download_report(
    complaint_id: str,
):

    pdf_path = Path(
        "generated_reports"
    ) / f"{complaint_id}.pdf"

    if not pdf_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Report not found.",
        )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename=f"IFSO_Report_{complaint_id}.pdf",
    )