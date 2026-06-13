from fastapi import status

RESOURCES_ENDPOINT = "/api/v1/resources"


def test_list_resources_empty(client):
    response = client.get(RESOURCES_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_and_list_resource(client):
    payload = {
        "name": "CyberTipline",
        "url": "https://www.cybertipline.org/",
        "country": "US",
    }
    response = client.post(RESOURCES_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]

    response = client.get(RESOURCES_ENDPOINT)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
