from fastapi import status

from app.models import Institution
from app.services.auth import hash_password


class TestAdminDigest:
    def test_send_all_digest_requires_supervisor(self, client, auth_headers):
        response = client.post("/api/v1/admin/digest/send-all", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_send_all_digest_unconfigured_smtp(
        self, client, db_session, supervisor_headers
    ):
        inst = Institution(
            name="Test Org Digest",
            code="DIGEST01",
            api_key_hash=hash_password("key"),
            contact_email="ops@example.org",
            contract_active=True,
            alert_config={},
        )
        db_session.add(inst)
        db_session.commit()

        response = client.post(
            "/api/v1/admin/digest/send-all", headers=supervisor_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["sent"]) == 1
        assert data["sent"][0]["sent"] is False
