from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services.auth import get_current_user, hash_password, require_role
from app.services.rate_limit import check_rate_limit
from app.services.totp_service import disable_totp, enable_totp, verify_code

router = APIRouter(prefix="/users", tags=["admin-users"])


@router.get("", response_model=list[UserResponse])
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    return db.query(User).all()


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    request: Request,
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Usuario ya existe")
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/me/totp/setup")
def setup_totp(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    return enable_totp(db, current_user)


@router.post("/me/totp/verify")
def verify_totp(
    request: Request,
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="TOTP no configurado")
    if not verify_code(current_user.totp_secret, code):
        raise HTTPException(status_code=401, detail="Código TOTP inválido")
    return {"valid": True}


@router.delete("/me/totp/disable")
def delete_totp(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    disable_totp(db, current_user)
    return {"enabled": False}
