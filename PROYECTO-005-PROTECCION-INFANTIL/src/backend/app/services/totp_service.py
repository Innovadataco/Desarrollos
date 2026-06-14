"""Servicio de 2FA TOTP para usuarios administrativos."""

import base64
import io

import pyotp
import qrcode
from sqlalchemy.orm import Session

from app.models import User

TOTP_ISSUER = "SemaforoConfianza"


def generate_secret() -> str:
    return pyotp.random_base32()


def get_provisioning_uri(user: User, secret: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.username,
        issuer_name=TOTP_ISSUER,
    )


def generate_qr_code(uri: str) -> str:
    """Genera un QR como data URI PNG."""
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return (
        f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    )


def verify_code(secret: str, code: str) -> bool:
    if not secret or not code:
        return False
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def enable_totp(db: Session, user: User) -> dict:
    secret = generate_secret()
    user.totp_secret = secret
    user.totp_enabled = True
    db.commit()
    db.refresh(user)
    uri = get_provisioning_uri(user, secret)
    qr = generate_qr_code(uri)
    return {"secret": secret, "qr_code": qr, "enabled": True}


def disable_totp(db: Session, user: User) -> None:
    user.totp_secret = None
    user.totp_enabled = False
    db.commit()


def validate_user_totp(db: Session, user_id: str, code: str) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.totp_enabled or not user.totp_secret:
        return False
    return verify_code(user.totp_secret, code)
