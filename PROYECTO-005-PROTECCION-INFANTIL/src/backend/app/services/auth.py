from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": username,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def get_current_user(
    request: Request,
    credentials: HTTPBasicCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[len("Bearer ") :]
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Token inválido")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
    elif credentials:
        username = credentials.username
    else:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo o no existe")
    return user


def require_role(role: str):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        role_levels = {"viewer": 1, "supervisor": 2, "admin": 3}
        required = role_levels.get(role, 3)
        current = role_levels.get(current_user.role, 0)
        if current < required:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return current_user

    return checker
