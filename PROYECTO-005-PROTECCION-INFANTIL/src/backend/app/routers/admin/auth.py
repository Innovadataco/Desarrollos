from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse
from app.services.auth import create_access_token, verify_password
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/auth", tags=["admin-auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    check_rate_limit(request, scope="login", identifier=payload.username)

    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    access_token = create_access_token(user.username, user.role)
    return TokenResponse(access_token=access_token, token_type="bearer")
