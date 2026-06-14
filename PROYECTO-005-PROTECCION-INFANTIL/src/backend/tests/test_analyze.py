from fastapi import status

REPORT_ENDPOINT = "/api/v1/reportes"
ANALYZE_ENDPOINT = "/api/v1/analyze"


def test_analysis_runs_automatically_on_report(client, auth_headers):
    response = client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": "+573009999999",
            "description": "Le pidieron fotos a mi hija y dijeron que no le contara a nadie.",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    report_hash = response.json()["report_hash"]

    # Consulta debe reflejar score y nivel
    client.get(f"/api/v1/validate/{report_hash}")
    # No validamos score exacto porque depende del modelo, pero debe tener level
    report = client.get(f"/api/v1/admin/reports/{report_hash}", headers=auth_headers)
    assert report.status_code == status.HTTP_200_OK
    data = report.json()
    assert data["level"] in ("high", "critical", "severe", "medium", "low")


def test_get_analysis_requires_auth(client):
    response = client.get(f"{ANALYZE_ENDPOINT}/no-existe")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_analysis_requires_supervisor(client, auth_headers):
    response = client.post(f"{ANALYZE_ENDPOINT}/no-existe", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_analysis_creates_analysis(client, supervisor_headers):
    response = client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": "+573008888888",
            "description": "Amenazaron con difundir fotos si no enviaba más contenido.",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    report_hash = response.json()["report_hash"]

    analysis_response = client.post(
        f"{ANALYZE_ENDPOINT}/{report_hash}", headers=supervisor_headers
    )
    assert analysis_response.status_code == status.HTTP_200_OK
    data = analysis_response.json()
    assert data["score"] >= 0.0
    assert data["level"] in ("low", "medium", "high", "critical", "severe")
    assert data["category"] in {
        "contacto_inapropiado",
        "solicitud_material",
        "grooming",
        "cita_persona",
        "extorsion",
        "desconocido",
    }
