from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Report, User
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

from . import alerts, analytics, config, reports, users

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

router.include_router(alerts.router)
router.include_router(analytics.router)
router.include_router(config.router)
router.include_router(reports.router)
router.include_router(users.router)


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    total_reports = db.query(Report).count()
    pending = db.query(Report).filter(Report.status == "received").count()
    pending_analysis = (
        db.query(Report).filter(Report.status == "pending_analysis").count()
    )
    severe = db.query(Report).filter(Report.level == "severe").count()
    critical = db.query(Report).filter(Report.level == "critical").count()
    high = db.query(Report).filter(Report.level == "high").count()
    network = db.query(Report).filter(Report.is_network.is_(True)).count()
    return {
        "total_reports": total_reports,
        "pending": pending,
        "pending_analysis": pending_analysis,
        "severe": severe,
        "critical": critical,
        "high": high,
        "network": network,
    }
