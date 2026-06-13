from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SystemConfig, User
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/config", tags=["admin-config"])


class ConfigUpdate(BaseModel):
    threshold_severe: float | None = None
    threshold_critical: float | None = None
    threshold_high: float | None = None
    threshold_medium: float | None = None
    alert_severe_immediate: bool | None = None
    alert_critical_4h: bool | None = None
    alert_high_24h: bool | None = None
    alert_medium_weekly: bool | None = None


def _get_or_create(db: Session) -> SystemConfig:
    config = db.query(SystemConfig).first()
    if not config:
        config = SystemConfig()
        db.add(config)
        db.flush()
    return config


@router.get("")
def get_config(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    config = _get_or_create(db)
    return {
        "threshold_severe": config.threshold_severe,
        "threshold_critical": config.threshold_critical,
        "threshold_high": config.threshold_high,
        "threshold_medium": config.threshold_medium,
        "alert_severe_immediate": config.alert_severe_immediate,
        "alert_critical_4h": config.alert_critical_4h,
        "alert_high_24h": config.alert_high_24h,
        "alert_medium_weekly": config.alert_medium_weekly,
        "alert_network_immediate": config.alert_network_immediate,
        "digest_daily_time": config.digest_daily_time,
        "digest_weekly_day": config.digest_weekly_day,
        "digest_weekly_time": config.digest_weekly_time,
    }


@router.patch("")
def update_config(
    request: Request,
    payload: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    config = _get_or_create(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, field, value)
    config.updated_at = datetime.now(timezone.utc)
    config.updated_by = current_user.id
    db.commit()
    return get_config(request, db, current_user)
