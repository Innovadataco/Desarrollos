from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Report, User
from app.schemas import ReportStatusUpdate
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/reports", tags=["admin-reports"])


@router.get("")
def list_reports(
    request: Request,
    status: str | None = None,
    level: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    query = db.query(Report)
    if status:
        query = query.filter(Report.status == status)
    if level:
        query = query.filter(Report.level == level)
    return query.order_by(Report.reported_at.desc()).limit(200).all()


@router.get("/{report_hash}")
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
    return report


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
    report.status = payload.status
    report.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)
    return report
