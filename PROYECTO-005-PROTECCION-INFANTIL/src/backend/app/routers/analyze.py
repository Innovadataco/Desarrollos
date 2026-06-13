from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis, Report, User
from app.schemas import AnalysisResponse
from app.services.analysis_service import analyze_report
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/analyze", tags=["analyze"])


@router.get("/{report_id}", response_model=AnalysisResponse)
def get_analysis(
    request: Request,
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    analysis = (
        db.query(Analysis)
        .filter(Analysis.report_id == report.id)
        .order_by(Analysis.created_at.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    return analysis


@router.post("/{report_id}", response_model=AnalysisResponse)
def analyze_report_endpoint(
    request: Request,
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return analyze_report(report, db, actor=current_user.username)
