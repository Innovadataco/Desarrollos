import pytest

from app.models import Institution
from app.services.auth import hash_password


@pytest.fixture
def institution(db_session):
    inst = Institution(
        name="Test Org",
        code="TEST01",
        api_key_hash=hash_password("super-secret-key"),
        contact_email="ops@test.org",
        contract_active=True,
        alert_config={"levels": ["severe", "critical"]},
    )
    db_session.add(inst)
    db_session.commit()
    return inst


@pytest.fixture
def gateway_headers():
    return {"X-API-Key": "super-secret-key"}


class TestGatewayAuth:
    def test_missing_api_key(self, client):
        response = client.post("/api/v1/gateway/reports", json={"report_hash": "abc"})
        assert response.status_code == 401

    def test_invalid_api_key(self, client):
        response = client.post(
            "/api/v1/gateway/reports",
            json={"report_hash": "abc"},
            headers={"X-API-Key": "bad"},
        )
        assert response.status_code == 401


class TestGatewayReport:
    def test_summary_not_found(self, client, institution, gateway_headers):
        response = client.post(
            "/api/v1/gateway/reports",
            json={"report_hash": "unknown"},
            headers=gateway_headers,
        )
        assert response.status_code == 404

    def test_summary_success(self, client, institution, gateway_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "testuser@example.com",
                "description": "Contenido sospechoso",
                "category": "grooming",
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        report_hash = report_resp.json()["report_hash"]

        response = client.post(
            "/api/v1/gateway/reports",
            json={"report_hash": report_hash, "request_type": "summary"},
            headers=gateway_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["report_hash"] == report_hash
        assert data["identifier_type"] == "email"
        assert "score" in data

    def test_full_success(self, client, institution, gateway_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "+573001234567",
                "description": "Contenido sospechoso",
                "category": "grooming",
                "consent_location": True,
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        report_hash = report_resp.json()["report_hash"]

        response = client.post(
            "/api/v1/gateway/reports",
            json={"report_hash": report_hash, "request_type": "full"},
            headers=gateway_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "profile" in data
        if data.get("profile"):
            assert abs(data["profile"]["score"] - data["score"]) < 0.01


class TestGatewayDigest:
    def test_digest_counts(self, client, institution, gateway_headers):
        client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "digest@test.org",
                "description": "Contenido sospechoso grave",
                "category": "grooming",
            },
        )
        response = client.post(
            "/api/v1/gateway/digest",
            json={"period": "daily", "date": "2026-06-13"},
            headers=gateway_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["report_count"] >= 1
        assert "severe_count" in data


class TestGatewayNCMECExport:
    def test_ncmec_export_success(self, client, institution, gateway_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "ncmec@test.org",
                "description": "Contenido grave",
                "category": "grooming",
            },
        )
        report_hash = report_resp.json()["report_hash"]
        response = client.post(
            "/api/v1/gateway/ncmec-export",
            json={"report_hash": report_hash},
            headers=gateway_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["format"] == "ncmec-like"
        assert data["report_hash"] == report_hash
        assert data["reporting_person"]["anonymous"] is True


class TestGatewayDigestSend:
    def test_send_digest_unconfigured_smtp(self, client, institution, gateway_headers):
        response = client.post(
            "/api/v1/gateway/digest/send",
            headers=gateway_headers,
        )
        assert response.status_code == 200
        assert response.json()["sent"] is False


class TestGatewayConfirm:
    def test_confirm_success(self, client, institution, gateway_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "confirm@test.org",
                "description": "Otro contenido",
                "category": "otro",
            },
        )
        report_hash = report_resp.json()["report_hash"]
        response = client.post(
            "/api/v1/gateway/confirm",
            json={"report_hash": report_hash, "status": "received"},
            headers=gateway_headers,
        )
        assert response.status_code == 200
        assert response.json()["confirmed"] is True
