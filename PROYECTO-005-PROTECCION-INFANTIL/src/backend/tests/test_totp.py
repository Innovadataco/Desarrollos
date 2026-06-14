import pyotp
from fastapi import status


class TestTOTP:
    def test_setup_totp(self, client, auth_headers):
        response = client.post(
            "/api/v1/admin/users/me/totp/setup", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["enabled"] is True
        assert data["secret"]
        assert data["qr_code"].startswith("data:image/png;base64,")

    def test_verify_totp_valid(self, client, auth_headers, db_session, auth_user):
        setup = client.post("/api/v1/admin/users/me/totp/setup", headers=auth_headers)
        secret = setup.json()["secret"]
        code = pyotp.TOTP(secret).now()

        response = client.post(
            f"/api/v1/admin/users/me/totp/verify?code={code}",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["valid"] is True

    def test_verify_totp_invalid(self, client, auth_headers, db_session, auth_user):
        client.post("/api/v1/admin/users/me/totp/setup", headers=auth_headers)
        response = client.post(
            "/api/v1/admin/users/me/totp/verify?code=000000",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_disable_totp(self, client, auth_headers):
        client.post("/api/v1/admin/users/me/totp/setup", headers=auth_headers)
        response = client.delete(
            "/api/v1/admin/users/me/totp/disable", headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["enabled"] is False
