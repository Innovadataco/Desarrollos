from fastapi import status

REPORT_ENDPOINT = "/api/v1/reportes"
CONSULTA_ENDPOINT = "/api/v1/consultas"


def test_consulta_not_found(client):
    response = client.post(CONSULTA_ENDPOINT, json={"identifier": "+57300000000"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "not_found"
    assert data["level"] == "low"


def test_consulta_found_after_report(client):
    identifier = "+573001234567"
    client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": identifier,
            "description": "Descripción de prueba suficiente",
        },
    )
    response = client.post(CONSULTA_ENDPOINT, json={"identifier": identifier})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "found"
    assert data["report_count"] == 1
