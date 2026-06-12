from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Report
from app.schemas import ReportCreate, ReportResponse
from app.services.encryption import derive_kek, encrypt_field, generate_report_hash
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/reportes", tags=["reportes"])

kek = derive_kek(settings.report_encryption_key)

MAX_HASH_RETRIES = 5


@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un reporte anónimo",
)
def create_report(
    request: Request,
    payload: ReportCreate,
    db: Session = Depends(get_db),
):
    check_rate_limit(request)

    reported_at = datetime.now(timezone.utc)
    reported_identifier_cipher = encrypt_field(payload.reported_identifier, kek)
    description_cipher = encrypt_field(payload.description, kek)
    evidence_type = payload.evidence.type if payload.evidence else None
    evidence_content_cipher = (
        encrypt_field(payload.evidence.content, kek) if payload.evidence else None
    )

    for attempt in range(MAX_HASH_RETRIES):
        report_hash = generate_report_hash(
            payload.reported_identifier,
            reported_at.isoformat(),
        )
        report = Report(
            report_hash=report_hash,
            reported_identifier=reported_identifier_cipher,
            description=description_cipher,
            evidence_type=evidence_type,
            evidence_content=evidence_content_cipher,
            reported_at=reported_at,
            updated_at=reported_at,
        )
        db.add(report)
        try:
            db.commit()
            db.refresh(report)
            return ReportResponse(
                report_hash=report.report_hash,
                reported_at=report.reported_at.isoformat(),
            )
        except IntegrityError:
            db.rollback()
            if attempt == MAX_HASH_RETRIES - 1:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="No se pudo generar un identificador único para el reporte.",
                )
