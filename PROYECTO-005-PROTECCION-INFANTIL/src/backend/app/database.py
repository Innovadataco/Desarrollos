from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from app.config import settings

_db_url = settings.database_url
_connect_args = {}
_pool_kwargs = {}

if _db_url.startswith("sqlite"):
    _connect_args["check_same_thread"] = False
    if ":memory:" in _db_url:
        _pool_kwargs["poolclass"] = StaticPool

engine = create_engine(
    _db_url, pool_pre_ping=True, connect_args=_connect_args, **_pool_kwargs
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    _ensure_root_user()


def _ensure_root_user():
    """Crea el usuario root si no existe ningún usuario en la base de datos."""
    from app.models import User
    from app.services.auth import hash_password

    db = SessionLocal()
    try:
        existing = db.query(User).first()
        if existing:
            return
        root = User(
            username="root",
            password_hash=hash_password(settings.admin_root_password),
            role="admin",
            is_active=True,
        )
        db.add(root)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
