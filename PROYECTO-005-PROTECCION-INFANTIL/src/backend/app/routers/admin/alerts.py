from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, User
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/alerts", tags=["admin-alerts"])


@router.get("")
def list_admin_alerts(
    request: Request,
    status: str = "open",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    return (
        db.query(Alert)
        .filter(Alert.status == status)
        .order_by(Alert.created_at.desc())
        .limit(100)
        .all()
    )
