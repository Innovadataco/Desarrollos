from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Report, User
from app.schemas import (
    AdminReportDetail,
    AdminReportListItem,
    DecryptRequest,
    DecryptResponse,
    ReportStatusUpdate,
)
from app.services.auth import require_role
from app.services.encryption import decrypt_field
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/reports", tags=["admin-reports"])


def _has_evidence(report: Report) -> bool:
    return report.evidence_content is not None and len(report.evidence_content) > 0


@router.get("", response_model=list[AdminReportListItem])
def list_reports(
    request: Request,
    status: str | None = None,
    level: str | None = None,
    category: str | None = None,
    city: str | None = None,
    country: str | None = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    query = db.query(Report)
    if status:
        query = query.filter(Report.status == status)
    if level:
        query = query.filter(Report.level == level)
    if category:
        query = query.filter(Report.category == category)
    if city:
        query = query.filter(Report.city == city)
    if country:
        query = query.filter(Report.country == country)

    reports = (
        query.order_by(Report.reported_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return [
        AdminReportListItem(
            id=r.id,
            report_hash=r.report_hash,
            reported_at=r.reported_at,
            score=r.score,
            level=r.level,
            category=r.category,
            status=r.status,
            city=r.city,
            country=r.country,
            evidence_type=r.evidence_type,
            has_evidence=_has_evidence(r),
        )
        for r in reports
    ]


@router.get("/{report_hash}", response_model=AdminReportDetail)
def get_report(
    request: Request,
    report_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return AdminReportDetail(
        id=report.id,
        report_hash=report.report_hash,
        reported_at=report.reported_at,
        updated_at=report.updated_at,
        score=report.score,
        level=report.level,
        category=report.category,
        status=report.status,
        city=report.city,
        country=report.country,
        evidence_type=report.evidence_type,
        identifier_type=report.identifier_type,
        identifier_hash=report.identifier_hash,
        has_evidence=_has_evidence(report),
    )


@router.patch("/{report_hash}/status")
def update_report_status(
    request: Request,
    report_hash: str,
    payload: ReportStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    old_status = report.status
    report.status = payload.status
    report.updated_at = datetime.now(timezone.utc)

    audit = AuditLog(
        action="status_change",
        actor_hash=str(current_user.id),
        report_hash=report.report_hash,
        details=f"{old_status} -> {payload.status}; notes={payload.notes}",
    )
    db.add(audit)
    db.commit()
    db.refresh(report)
    return AdminReportDetail(
        id=report.id,
        report_hash=report.report_hash,
        reported_at=report.reported_at,
        updated_at=report.updated_at,
        score=report.score,
        level=report.level,
        category=report.category,
        status=report.status,
        city=report.city,
        country=report.country,
        evidence_type=report.evidence_type,
        identifier_type=report.identifier_type,
        identifier_hash=report.identifier_hash,
        has_evidence=_has_evidence(report),
    )


@router.post("/{report_hash}/decrypt", response_model=DecryptResponse)
def decrypt_report(
    request: Request,
    report_hash: str,
    payload: DecryptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("reviewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    from app.config import settings

    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    kek = settings.encryption_kek()
    reported_identifier = decrypt_field(report.reported_identifier, kek)
    description = decrypt_field(report.description, kek)
    evidence_content = None
    if report.evidence_content:
        evidence_content = decrypt_field(report.evidence_content, kek)

    audit = AuditLog(
        action="decrypt",
        actor_hash=str(current_user.id),
        report_hash=report.report_hash,
        details=payload.reason,
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    return DecryptResponse(
        decrypted_at=datetime.now(timezone.utc).isoformat(),
        reported_identifier=reported_identifier,
        description=description,
        evidence_content=evidence_content,
        evidence_type=report.evidence_type,
        audit_log_id=str(audit.id),
    )
