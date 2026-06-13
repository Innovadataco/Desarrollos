from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Report, User
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/analytics", tags=["admin-analytics"])


@router.get("/summary")
def summary(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    total = db.query(Report).count()
    today = datetime.now(timezone.utc).date()
    today_start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    today_count = db.query(Report).filter(Report.reported_at >= today_start).count()
    levels = db.query(Report.level, func.count(Report.id)).group_by(Report.level).all()
    categories = (
        db.query(Report.category, func.count(Report.id)).group_by(Report.category).all()
    )
    return {
        "total_reports": total,
        "today_reports": today_count,
        "by_level": {level: count for level, count in levels},
        "by_category": {cat: count for cat, count in categories},
    }


@router.get("/trends")
def trends(
    request: Request,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    since = datetime.now(timezone.utc) - timedelta(days=days)
    rows = (
        db.query(func.date(Report.reported_at), func.count(Report.id))
        .filter(Report.reported_at >= since)
        .group_by(func.date(Report.reported_at))
        .all()
    )
    return {"days": days, "trend": [{"date": str(d), "count": c} for d, c in rows]}
