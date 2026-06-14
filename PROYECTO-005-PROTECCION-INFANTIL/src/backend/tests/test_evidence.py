from io import BytesIO

import pytest
from fastapi import status

REPORT_ENDPOINT = "/api/v1/reportes"


@pytest.fixture
def report(client):
    response = client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": "evidence@test.org",
            "description": "Incidente con archivo adjunto",
            "category": "CAT-03",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["report_hash"]


class TestEvidenceUpload:
    def test_upload_png(self, client, report):
        response = client.post(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            files={
                "file": ("screenshot.png", BytesIO(b"fake-png-content"), "image/png")
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["report_hash"] == report
        assert data["kind"] == "png"

    def test_upload_pdf(self, client, report):
        response = client.post(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            files={
                "file": (
                    "documento.pdf",
                    BytesIO(b"fake-pdf-content"),
                    "application/pdf",
                )
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["kind"] == "pdf"

    def test_upload_invalid_type(self, client, report):
        response = client.post(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            files={
                "file": ("virus.exe", BytesIO(b"fake-exe"), "application/octet-stream")
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_report_not_found(self, client):
        response = client.post(
            f"{REPORT_ENDPOINT}/0000000000000000000000000000000000000000000000000000000000000000/evidence",
            files={"file": ("foto.png", BytesIO(b"x"), "image/png")},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_evidence(self, client, report, auth_headers):
        client.post(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            files={"file": ("foto.png", BytesIO(b"x"), "image/png")},
        )
        response = client.get(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["filename"] == "foto.png"

    def test_download_evidence(self, client, report, auth_headers):
        upload = client.post(
            f"{REPORT_ENDPOINT}/{report}/evidence",
            files={"file": ("foto.png", BytesIO(b"contenido-imagen"), "image/png")},
        )
        evidence_id = upload.json()["evidence_id"]
        response = client.get(
            f"{REPORT_ENDPOINT}/{report}/evidence/{evidence_id}",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.content == b"contenido-imagen"
