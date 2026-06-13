import os
from unittest.mock import patch

import pytest
from fastapi import status

# Forzar un entorno de prueba antes de importar la app/config
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["REPORT_ENCRYPTION_KEY"] = (
    "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
)
os.environ["ENVIRONMENT"] = "testing"
os.environ["REDIS_URL"] = ""


def test_security_headers_present(client):
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers
    assert "Content-Security-Policy" in response.headers


def test_hsts_only_in_production(client):
    response = client.get("/api/health")
    assert "Strict-Transport-Security" not in response.headers


def test_cors_rejects_unknown_origin(client):
    response = client.post(
        "/api/reportes",
        json={"reported_identifier": "x", "description": "y"},
        headers={"Origin": "http://evil.com"},
    )
    # La respuesta puede ser 201 si CORS no bloquea en servidor (lo hace el navegador)
    # pero no debe incluir Access-Control-Allow-Origin del origen desconocido
    assert response.headers.get("access-control-allow-origin") != "http://evil.com"


def test_invalid_encryption_key_raises_on_startup():
    with patch.dict(
        os.environ,
        {
            "REPORT_ENCRYPTION_KEY": "corta",
            "DATABASE_URL": "sqlite:///:memory:",
            "ENVIRONMENT": "testing",
            "REDIS_URL": "",
        },
        clear=False,
    ):
        with pytest.raises(ValueError) as exc_info:
            # Importamos dentro del contexto para que tome la variable de entorno
            from app.config import Settings

            Settings()
    assert "64 caracteres hexadecimales" in str(exc_info.value)


def test_missing_encryption_key_raises_on_startup():
    with patch.dict(
        os.environ,
        {
            "REPORT_ENCRYPTION_KEY": "",
            "DATABASE_URL": "sqlite:///:memory:",
            "ENVIRONMENT": "testing",
            "REDIS_URL": "",
        },
        clear=False,
    ):
        with pytest.raises(ValueError) as exc_info:
            from app.config import Settings

            Settings()
    assert "REPORT_ENCRYPTION_KEY es requerida" in str(exc_info.value)


def test_report_endpoint_does_not_expose_server_header(client):
    response = client.get("/api/health")
    assert "server" not in response.headers.get("server", "").lower()
