import os

# Forzar SQLite en memoria y clave de encriptación de prueba antes de importar la app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REPORT_ENCRYPTION_KEY"] = (
    "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
)
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-signing-only"
os.environ["ADMIN_ROOT_PASSWORD"] = "testrootpassword"
os.environ["ENVIRONMENT"] = "testing"
os.environ["REDIS_URL"] = ""
os.environ["CORS_ORIGINS"] = "http://localhost:5173"
os.environ["ALLOWED_HOSTS"] = "testserver,localhost,127.0.0.1"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database as database_module
from app.database import Base, get_db
from app.main import app
from app.models import User
from app.services.auth import create_access_token, hash_password
from app.services.rate_limit import reset_fallback_limiters


@pytest.fixture(scope="session", autouse=True)
def close_global_engine():
    """Cierra el engine global de la aplicación al terminar la sesión de tests."""
    yield
    database_module.engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(db_session):
    reset_fallback_limiters()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_user(db_session):
    user = User(
        username="viewer",
        password_hash=hash_password("viewerpass"),
        role="viewer",
        email="viewer@example.com",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def auth_supervisor(db_session):
    user = User(
        username="supervisor",
        password_hash=hash_password("supervisorpass"),
        role="supervisor",
        email="supervisor@example.com",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def auth_headers(auth_user):
    token = create_access_token(auth_user.username, auth_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def supervisor_headers(auth_supervisor):
    token = create_access_token(auth_supervisor.username, auth_supervisor.role)
    return {"Authorization": f"Bearer {token}"}
