import os

# Forzar SQLite en memoria y clave de encriptación de prueba antes de importar la app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REPORT_ENCRYPTION_KEY"] = (
    "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
)
os.environ["ENVIRONMENT"] = "testing"
os.environ["REDIS_URL"] = ""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database as database_module
from app.database import Base, get_db
from app.main import app
from app.services.rate_limit import _fallback_rate_limiter


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
    _fallback_rate_limiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
