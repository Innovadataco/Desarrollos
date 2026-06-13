import pytest
from fastapi import status


@pytest.fixture
def report(client):
    response = client.post(
        "/api/v1/reportes",
        json={
            "reported_identifier": "export@test.org",
            "description": "Mensajes inapropiados reiterados",
            "category": "grooming",
            "consent_location": True,
        },
        headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["report_hash"]


class TestExport:
    def test_export_json_requires_supervisor(self, client, auth_headers, report):
        response = client.get(
            f"/api/v1/admin/reports/{report}/export?format=json", headers=auth_headers
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_export_json_success(self, client, supervisor_headers, report):
        response = client.get(
            f"/api/v1/admin/reports/{report}/export?format=json",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["report_hash"] == report
        assert "identifier_hash" in data
        assert "exported_at" in data

    def test_export_pdf_success(self, client, supervisor_headers, report):
        response = client.get(
            f"/api/v1/admin/reports/{report}/export?format=pdf",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 100

    def test_export_with_encrypted_content(self, client, supervisor_headers, report):
        response = client.get(
            f"/api/v1/admin/reports/{report}/export?format=json&include_encrypted=true",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reported_identifier"] == "export@test.org"
        assert "description" in data

    def test_export_pdf_with_encrypted_content(self, client, supervisor_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "pdf-encrypt@test.org",
                "description": "Mensajes inapropiados",
                "category": "grooming",
                "evidence": {"type": "text", "content": "captura de pantalla"},
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        report_hash = report_resp.json()["report_hash"]
        response = client.get(
            f"/api/v1/admin/reports/{report_hash}/export?format=pdf&include_encrypted=true",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 100

    def test_export_invalid_format(self, client, supervisor_headers, report):
        response = client.get(
            f"/api/v1/admin/reports/{report}/export?format=xml",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestAuditTrail:
    def test_audit_logs_list(self, client, supervisor_headers, report):
        response = client.get(
            "/api/v1/admin/audit",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "logs" in data
        assert "total" in data

    def test_audit_logs_filter_by_report(self, client, supervisor_headers, report):
        # Forzar un decrypt para generar audit
        client.post(
            f"/api/v1/admin/reports/{report}/decrypt",
            json={"reason": "Auditoria de prueba para generar log"},
            headers=supervisor_headers,
        )
        response = client.get(
            f"/api/v1/admin/audit?report_hash={report}&action=decrypt",
            headers=supervisor_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] >= 1
        assert any(log["action"] == "decrypt" for log in data["logs"])
