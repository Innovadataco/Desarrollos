from fastapi import status

CONFIG_ENDPOINT = "/api/v1/admin/config"


def test_get_config_requires_auth(client):
    response = client.get(CONFIG_ENDPOINT)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_config(client, auth_headers):
    response = client.get(CONFIG_ENDPOINT, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "threshold_severe" in data
    assert "digest_daily_time" in data


def test_update_config_requires_supervisor(client, auth_headers):
    response = client.patch(
        CONFIG_ENDPOINT,
        json={"threshold_severe": 0.9},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_config(client, supervisor_headers):
    response = client.patch(
        CONFIG_ENDPOINT,
        json={"threshold_severe": 0.9},
        headers=supervisor_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["threshold_severe"] == 0.9
