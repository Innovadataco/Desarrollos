import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import AuditLog, Evidence, Identifier, Report
from app.schemas import ReportCreate, ReportResponse
from app.services.analysis_service import analyze_report
from app.services.encryption import encrypt_field, generate_report_hash
from app.services.identifier import detect_identifier_type, hash_identifier
from app.services.profile_service import update_profile_from_report
from app.services.rate_limit import check_rate_limit
from app.utils.time import truncate_to_hours

router = APIRouter(prefix="/api/v1/reportes", tags=["reportes"])
MAX_HASH_RETRIES = 5


def _check_rate_limit(request: Request, db: Session):
    client_ip = _get_client_ip(request)
    try:
        check_rate_limit(request, scope="report", identifier=client_ip)
    except HTTPException as exc:
        _log_audit(
            db,
            "rate_limit",
            _hash_ip(client_ip),
            None,
            f"HTTP {exc.status_code}: {exc.detail}",
        )
        raise


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()


def _log_audit(
    db: Session,
    action: str,
    actor_hash: str,
    report_hash: str | None,
    details: str,
):
    log = AuditLog(
        action=action,
        actor_hash=actor_hash,
        report_hash=report_hash,
        details=details,
    )
    db.add(log)


def _extract_location(request: Request):
    country = request.headers.get("x-client-country")
    city = request.headers.get("x-client-city")
    return city, country


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    request: Request,
    payload: ReportCreate,
    db: Session = Depends(get_db),
):
    _check_rate_limit(request, db)

    if payload.honeypot and payload.honeypot.strip():
        client_ip = _get_client_ip(request)
        _log_audit(
            db,
            "honeypot_triggered",
            _hash_ip(client_ip),
            None,
            "Campo honeypot completado",
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solicitud no válida.",
        )

    reported_at = datetime.now(timezone.utc)
    identifier_stripped = payload.reported_identifier.strip().lower()
    identifier_hash = hash_identifier(identifier_stripped)
    identifier_type = detect_identifier_type(payload.reported_identifier)

    # Encrypt personally identifiable data.
    reported_identifier_cipher = encrypt_field(
        payload.reported_identifier, settings.encryption_kek()
    )
    description_cipher = encrypt_field(payload.description, settings.encryption_kek())

    # Optional evidence encryption.
    evidence_type = None
    evidence_content_cipher = None
    if payload.evidence:
        evidence_type = payload.evidence.type
        evidence_content_cipher = encrypt_field(
            payload.evidence.content, settings.encryption_kek()
        )

    city, country = (None, None)
    if payload.consent_location:
        city, country = _extract_location(request)

    report = Report(
        identifier_hash=identifier_hash,
        identifier_type=identifier_type,
        reported_identifier=reported_identifier_cipher,
        description=description_cipher,
        category=payload.category or "otro",
        evidence_type=evidence_type,
        evidence_content=evidence_content_cipher,
        evidence_media_url=payload.evidence_media_url,
        city=city,
        country=country,
        consent_location=bool(payload.consent_location),
        reported_at=reported_at,
        reported_at_bucket=truncate_to_hours(reported_at, 6),
        status="received",
    )

    # Build evidence association if present.
    if payload.evidence:
        evidence = Evidence(
            report=report,
            kind=payload.evidence.type,
            content=evidence_content_cipher,
            source="user_upload",
        )
        db.add(evidence)

    # Upsert identifier profile stub.
    identifier = db.query(Identifier).filter(Identifier.hash == identifier_hash).first()
    if not identifier:
        identifier = Identifier(
            hash=identifier_hash,
            type=identifier_type,
            first_seen=reported_at,
            last_seen=reported_at,
            report_count=1,
        )
        db.add(identifier)
    else:
        identifier.last_seen = reported_at
        identifier.report_count += 1

    # Generate confirmation hash with collision retry.
    for attempt in range(MAX_HASH_RETRIES):
        report_hash = generate_report_hash(
            payload.reported_identifier,
            reported_at.isoformat(),
        )
        report.report_hash = report_hash
        db.add(report)
        try:
            db.commit()
            db.refresh(report)
            _log_audit(
                db,
                "report_created",
                _hash_ip(_get_client_ip(request)),
                report_hash,
                "Reporte recibido",
            )
            db.commit()
            try:
                analyze_report(report, db, actor="system")
                update_profile_from_report(report, db)
            except Exception:
                db.rollback()
            return ReportResponse(
                report_hash=report.report_hash,
                reported_at=report.reported_at_bucket.isoformat()
                if report.reported_at_bucket
                else report.reported_at.isoformat(),
                reported_at_bucket=report.reported_at_bucket.isoformat()
                if report.reported_at_bucket
                else None,
                message="Reporte recibido de forma segura. Guarda este código.",
            )
        except IntegrityError:
            db.rollback()
            if attempt == MAX_HASH_RETRIES - 1:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="No se pudo generar un identificador único",
                )
