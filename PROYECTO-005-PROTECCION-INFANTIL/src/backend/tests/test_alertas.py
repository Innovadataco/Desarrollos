from fastapi import status

REPORT_ENDPOINT = "/api/v1/reportes"
ALERTAS_ENDPOINT = "/api/v1/alertas"


def test_create_alert_requires_auth(client):
    response = client.post(
        ALERTAS_ENDPOINT,
        json={"report_hash": "x", "level": "high", "reason": "test"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_and_list_alert(client, supervisor_headers):
    report = client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": "+573001234567",
            "description": "Descripción de prueba suficiente",
        },
    ).json()
    response = client.post(
        ALERTAS_ENDPOINT,
        json={
            "report_hash": report["report_hash"],
            "level": "high",
            "reason": "Revisión prioritaria",
        },
        headers=supervisor_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["level"] == "high"

    response = client.get(ALERTAS_ENDPOINT, headers=supervisor_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
