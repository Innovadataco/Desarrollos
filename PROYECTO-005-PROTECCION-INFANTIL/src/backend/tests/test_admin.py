from fastapi import status

ADMIN_DASHBOARD = "/api/v1/admin/dashboard"
ADMIN_ANALYTICS = "/api/v1/admin/analytics/summary"
ADMIN_REPORTS = "/api/v1/admin/reports"
ADMIN_USERS = "/api/v1/admin/users"


def test_dashboard_requires_auth(client):
    response = client.get(ADMIN_DASHBOARD)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_dashboard_viewer(client, auth_headers):
    response = client.get(ADMIN_DASHBOARD, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_reports" in data


def test_analytics_summary(client, auth_headers):
    response = client.get(ADMIN_ANALYTICS, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_reports" in data
    assert "by_level" in data


def test_list_reports(client, auth_headers):
    response = client.get(ADMIN_REPORTS, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_user_requires_admin(client, auth_headers):
    response = client.post(
        ADMIN_USERS,
        json={"username": "new", "password": "newpass12", "role": "viewer"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
