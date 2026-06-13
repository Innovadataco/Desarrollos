import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, User
from app.schemas import AlertCreate, AlertResponse, AlertUpdate
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/alertas", tags=["alertas"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    request: Request,
    level: str | None = None,
    status: str = "open",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    query = db.query(Alert).filter(Alert.status == status)
    if level:
        query = query.filter(Alert.level == level)
    return query.order_by(Alert.created_at.desc()).limit(100).all()


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(
    request: Request,
    payload: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    alert = Alert(
        report_hash=payload.report_hash,
        level=payload.level,
        reason=payload.reason,
        status="open",
        created_at=datetime.now(timezone.utc),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    request: Request,
    alert_id: str,
    payload: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    alert = db.query(Alert).filter(Alert.id == uuid.UUID(alert_id)).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(alert, field, value)
    alert.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)
    return alert
