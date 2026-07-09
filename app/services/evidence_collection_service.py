from __future__ import annotations

from app.services.evidence_models import (
    EvidenceCollection,
    UploadedEvidence,
)


class EvidenceCollectionService:

    def initialize(
        self,
        required: list[str],
    ) -> EvidenceCollection:

        return EvidenceCollection(

            required=sorted(set(required)),

            missing=sorted(set(required)),

            uploaded=[],

            completed=False,
        )

    def upload(
        self,
        collection: EvidenceCollection,
        *,
        evidence_type: str,
        filename: str,
        file_path: str,
    ) -> EvidenceCollection:

        uploaded = UploadedEvidence(

            evidence_type=evidence_type,

            filename=filename,

            file_path=file_path,
        )

        collection.uploaded.append(uploaded)

        uploaded_types = {

            item.evidence_type

            for item in collection.uploaded

        }

        collection.missing = [

            item

            for item in collection.required

            if item not in uploaded_types

        ]

        collection.completed = (

            len(collection.missing) == 0

        )

        return collection

    def status(
        self,
        collection: EvidenceCollection,
    ):

        return {

            "required": collection.required,

            "uploaded": [

                {

                    "id": item.evidence_id,

                    "type": item.evidence_type,

                    "filename": item.filename,

                    "uploaded_at": item.uploaded_at,

                }

                for item in collection.uploaded

            ],

            "missing": collection.missing,

            "completed": collection.completed,

            "progress": {

                "uploaded": len(collection.uploaded),

                "required": len(collection.required),

            },
        }