from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import AuditLogListResponse
from app.services.auth import require_role
from app.services.export_service import list_audit_logs
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/audit", tags=["admin-audit"])


@router.get("", response_model=AuditLogListResponse)
def get_audit_logs(
    request: Request,
    report_hash: str | None = None,
    action: str | None = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    return list_audit_logs(
        db, report_hash=report_hash, action=action, page=page, limit=limit
    )
