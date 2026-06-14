from fastapi import status


class TestIAAudit:
    def test_model_card(self, client, auth_headers):
        response = client.get("/api/v1/analyze/model-card", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["version"]
        assert "metrics" in data
        assert "limitations" in data

    def test_fairness_audit(self, client, auth_headers):
        response = client.get("/api/v1/analyze/fairness", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "scores" in data
        assert "score_spread" in data
        assert "bias_flag" in data

    def test_redteam_requires_supervisor(self, client, auth_headers):
        response = client.get("/api/v1/analyze/redteam", headers=auth_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_redteam_audit(self, client, supervisor_headers):
        response = client.get("/api/v1/analyze/redteam", headers=supervisor_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["prompts_tested"] >= 6
        assert "flagged" in data
        assert "missed_adversarial" in data
