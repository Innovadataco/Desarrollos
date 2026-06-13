from fastapi import status

REPORT_ENDPOINT = "/api/v1/reportes"
CONSULTA_ENDPOINT = "/api/v1/consultas"
VALIDATE_ENDPOINT = "/api/v1/validate"


def test_consulta_not_found(client):
    response = client.post(CONSULTA_ENDPOINT, json={"identifier": "+57300000000"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "verde"
    assert data["report_count"] == 0


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
    assert data["semaforo"] == "amarillo"
    assert data["report_count"] == 1


def test_validate_not_found(client):
    response = client.get(f"{VALIDATE_ENDPOINT}/+57300000000")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "verde"
    assert data["report_count"] == 0


def test_validate_green(client):
    response = client.get(f"{VALIDATE_ENDPOINT}/@usuario_nuevo")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "verde"
    assert data["report_count"] == 0


def test_validate_yellow_after_one_report(client):
    identifier = "+573001111111"
    client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": identifier,
            "description": "Descripción de prueba suficiente",
        },
    )
    response = client.get(f"{VALIDATE_ENDPOINT}/{identifier}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "amarillo"
    assert data["report_count"] == 1


def test_validate_red_after_three_reports(client):
    identifier = "+573002222222"
    for _ in range(3):
        client.post(
            REPORT_ENDPOINT,
            json={
                "reported_identifier": identifier,
                "description": "Descripción de prueba suficiente",
            },
        )
    response = client.get(f"{VALIDATE_ENDPOINT}/{identifier}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "rojo"
    assert data["report_count"] == 3


def test_validate_network_by_cities(client):
    identifier = "+573003333333"
    cities = ["Bogota", "Medellin", "Cali"]
    for city in cities:
        client.post(
            REPORT_ENDPOINT,
            json={
                "reported_identifier": identifier,
                "description": "Descripción de prueba suficiente",
                "consent_location": True,
            },
            headers={"x-client-city": city, "x-client-country": "Colombia"},
        )
    response = client.get(f"{VALIDATE_ENDPOINT}/{identifier}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["semaforo"] == "negro"
    assert data["is_network"] is True
    assert data["cities_count"] == 3


def test_consulta_uses_cache(client):
    # Primera consulta
    response1 = client.post(
        CONSULTA_ENDPOINT, json={"identifier": "cached@example.com"}
    )
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()["report_count"] == 0

    # Crear reporte con el mismo identificador
    client.post(
        REPORT_ENDPOINT,
        json={
            "reported_identifier": "cached@example.com",
            "description": "Mensaje inapropiado",
            "category": "grooming",
        },
    )

    # Segunda consulta debe venir de cache (report_count=0)
    response2 = client.post(
        CONSULTA_ENDPOINT, json={"identifier": "cached@example.com"}
    )
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()["report_count"] == 0

    # Limpiar cache y volver a consultar
    from app.services.cache_service import clear

    clear()
    response3 = client.post(
        CONSULTA_ENDPOINT, json={"identifier": "cached@example.com"}
    )
    assert response3.status_code == status.HTTP_200_OK
    assert response3.json()["report_count"] == 1
