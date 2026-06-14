from fastapi import status

RESOURCES_ENDPOINT = "/api/v1/resources"


def test_list_resources_empty(client):
    response = client.get(RESOURCES_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_and_list_resource(client):
    response = client.post(
        RESOURCES_ENDPOINT,
        json={
            "name": "Línea 123",
            "url": "https://123.gov.co",
            "country": "Colombia",
            "phone": "123",
            "description": "Línea de emergencia",
            "priority": 1,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Línea 123"

    response = client.get(f"{RESOURCES_ENDPOINT}?country=Colombia")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
