from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.services.chatbot_service import (
    ChatbotService,
    get_chatbot_service,
)

router = APIRouter(
    prefix="/chat",
    tags=["Evidence Collection"],
)

UPLOAD_DIR = Path("uploads")


@router.post("/upload-evidence")
async def upload_evidence(

    session_id: str = Form(...),

    evidence_type: str = Form(...),

    file: UploadFile = File(...),

    chatbot: ChatbotService = Depends(
        get_chatbot_service
    ),
):

    session = chatbot.store.get(session_id)

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Invalid session.",
        )

    UPLOAD_DIR.mkdir(
        exist_ok=True,
    )

    filename = f"{uuid4()}_{file.filename}"

    destination = UPLOAD_DIR / filename

    with open(
        destination,
        "wb",
    ) as f:

        f.write(
            await file.read()
        )

    evidence = chatbot.investigation_service.evidence_collection.upload(

        session.evidence,

        evidence_type=evidence_type,

        filename=file.filename,

        file_path=str(destination),
    )

    session.evidence = evidence

    chatbot.store.update(session)

    # --------------------------------------------------------
    # Evidence collection completed
    # --------------------------------------------------------

    if evidence.completed:

        report = chatbot.investigation_service.investigate(

            description=session.description,

            incident_channel=session.fraud_channel,

            loss_amount=session.amount,
        )

        pdf_path = (
            f"generated_reports/"
            f"{report.complaint.complaint_id}.pdf"
        )

        from app.reports.pdf_generator import PDFGenerator

        PDFGenerator().generate(

            report,

            pdf_path,
        )

        return {

            "completed": True,

            "message": "Evidence collection completed successfully.",

            "investigation": report,

            "download_url": f"/report/download/{report.complaint.complaint_id}",

            "evidence": chatbot.investigation_service.evidence_collection.status(
                evidence
            ),
        }

    return {

        "completed": False,

        "message": "Evidence uploaded successfully.",

        "evidence": chatbot.investigation_service.evidence_collection.status(
            evidence
        ),
    }