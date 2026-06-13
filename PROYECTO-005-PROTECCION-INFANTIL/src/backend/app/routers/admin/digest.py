from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Institution, User
from app.services.auth import require_role
from app.services.email_service import send_digest_to_institution
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/digest", tags=["admin-digest"])


@router.post("/send-all")
async def send_all_digest(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("supervisor")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    today = datetime.now(timezone.utc).date()
    today_start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    results = []
    for institution in (
        db.query(Institution).filter(Institution.contract_active.is_(True)).all()
    ):
        result = await send_digest_to_institution(db, institution, today_start)
        results.append(result)
    return {"sent": results}
