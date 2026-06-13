import pytest

from app.models import Alert, Institution, Report
from app.services.email_service import (
    build_alert_body,
    build_digest_body,
    send_alert_to_institution,
    send_digest_to_institution,
)


@pytest.fixture
def institution(db_session):
    inst = Institution(
        name="Test",
        code="TEST",
        api_key_hash="x",
        contact_email="ops@test.org",
        contract_active=True,
        alert_config={},
    )
    db_session.add(inst)
    db_session.commit()
    return inst


class TestEmailService:
    @pytest.mark.asyncio
    async def test_send_alert_to_institution(self, db_session, institution):
        alert = Alert(report_hash="h" * 64, level="critical", reason="x")
        db_session.add(alert)
        db_session.commit()
        result = await send_alert_to_institution(db_session, alert)
        assert result["alert_id"]
        assert result["recipients"][0]["sent"] is False

    @pytest.mark.asyncio
    async def test_send_digest_to_institution(self, db_session, institution):
        from datetime import datetime, timezone

        result = await send_digest_to_institution(
            db_session, institution, datetime.now(timezone.utc)
        )
        assert result["institution"] == "TEST"
        assert result["sent"] is False

    def test_build_alert_body(self, db_session):
        report = Report(
            report_hash="h" * 64,
            reported_identifier=b"x",
            description=b"y",
            identifier_hash="ih",
            identifier_type="email",
            score=0.8,
            category="grooming",
            city="Bogota",
            country="CO",
        )
        db_session.add(report)
        db_session.commit()
        alert = Alert(
            report_id=report.id,
            report_hash=report.report_hash,
            level="critical",
            reason="Test alert",
        )
        db_session.add(alert)
        db_session.commit()
        body = build_alert_body(alert, report)
        assert "Alerta automática" in body
        assert "critical" in body

    def test_build_digest_body(self, institution):
        from datetime import datetime, timezone

        body = build_digest_body(
            institution,
            {
                "total": 5,
                "severe": 1,
                "critical": 1,
                "high": 1,
                "medium": 1,
                "low": 1,
                "network": 0,
            },
            datetime.now(timezone.utc),
        )
        assert "Digest Test" in body
        assert "Reportes nuevos: 5" in body
