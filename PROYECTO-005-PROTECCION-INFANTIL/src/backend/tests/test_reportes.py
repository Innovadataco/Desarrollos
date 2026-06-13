from unittest.mock import patch

from fastapi import status

from app.models import Report

REPORT_ENDPOINT = "/api/v1/reportes"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"


def test_create_report_success(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Recibí mensajes inapropiados",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "report_hash" in data
    assert len(data["report_hash"]) == 64
    assert "reported_at" in data

    report = db_session.query(Report).first()
    assert report is not None
    assert report.reported_identifier != payload["reported_identifier"].encode()
    assert report.description != payload["description"].encode()


def test_create_report_with_evidence(client, db_session):
    payload = {
        "reported_identifier": "@usuario_malo",
        "description": "Contacto inapropiado",
        "evidence": {
            "type": "text",
            "content": "captura de pantalla descriptiva",
        },
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    report = db_session.query(Report).first()
    assert report.evidence_type == "text"
    assert report.evidence_content is not None
    assert report.evidence_content != payload["evidence"]["content"].encode()


def test_create_report_with_image_evidence(client, db_session):
    payload = {
        "reported_identifier": "+573009998877",
        "description": "Imagen inapropiada",
        "evidence": {
            "type": "image",
            "content": "base64:fakeimagecontent",
        },
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    report = db_session.query(Report).first()
    assert report.evidence_type == "image"


def test_create_report_rejects_invalid_category_code(client):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Reporte con categoría inválida",
        "category": "CAT-99",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_report_maps_category_code_to_slug(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Reporte con categoría específica",
        "category": "CAT-03",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    report = db_session.query(Report).first()
    assert report.category == "grooming"


def test_create_report_with_evidence_media_url(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Enlace a evidencia externa",
        "evidence_media_url": "https://cdn.semaforo.com/enc/abc123",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["reported_at_bucket"] is not None

    report = db_session.query(Report).first()
    assert report.evidence_media_url == payload["evidence_media_url"]


def test_create_report_truncates_reported_at_to_6h_bucket(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Verificación de bucket temporal",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    report = db_session.query(Report).first()
    assert report.reported_at_bucket is not None
    assert data["reported_at"] == report.reported_at_bucket.isoformat()
    assert report.reported_at_bucket.minute == 0
    assert report.reported_at_bucket.second == 0
    assert report.reported_at_bucket.microsecond == 0


def test_create_report_missing_identifier(client):
    payload = {"description": "Solo descripción"}
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_report_invalid_evidence_type(client):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Incidente",
        "evidence": {"type": "video", "content": "contenido"},
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_report_missing_evidence_content(client):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Incidente",
        "evidence": {"type": "text"},
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_report_generates_unique_hashes(client):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Mismo identificador",
    }
    response1 = client.post(REPORT_ENDPOINT, json=payload)
    response2 = client.post(REPORT_ENDPOINT, json=payload)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED
    assert response1.json()["report_hash"] != response2.json()["report_hash"]


def test_create_report_handles_hash_collision(client, db_session):
    """Si generate_report_hash colisiona una vez, el endpoint debe reintentar."""
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Colisión controlada",
    }
    call_count = 0

    def colliding_hash(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return "a" * 64
        return "b" * 64

    db_session.add(
        Report(
            report_hash="a" * 64,
            reported_identifier=b"x",
            description=b"y",
            identifier_hash="ab" * 32,
            identifier_type="phone",
        )
    )
    db_session.commit()

    with patch("app.routers.reportes.generate_report_hash", side_effect=colliding_hash):
        response = client.post(REPORT_ENDPOINT, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["report_hash"] == "b" * 64
    assert call_count == 2


def test_create_report_gives_up_after_max_collision_retries(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Colisión persistente",
    }

    def always_collide(*args, **kwargs):
        return "a" * 64

    db_session.add(
        Report(
            report_hash="a" * 64,
            reported_identifier=b"x",
            description=b"y",
            identifier_hash="ab" * 32,
            identifier_type="phone",
        )
    )
    db_session.commit()

    with patch("app.routers.reportes.generate_report_hash", side_effect=always_collide):
        response = client.post(REPORT_ENDPOINT, json=payload)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_rate_limit_blocks_after_five_requests(client):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Reporte de prueba",
    }
    for _ in range(5):
        response = client.post(REPORT_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "límite" in response.json()["detail"].lower()


def test_rate_limit_does_not_persist_ip_after_reset(client):
    """El rate limiter en memoria no deja registro permanente de la IP."""
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Reporte de prueba",
    }
    for _ in range(5):
        response = client.post(REPORT_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    from app.services.rate_limit import reset_fallback_limiters

    reset_fallback_limiters()

    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_rate_limit_hashes_ip_in_fallback_storage(client):
    """El rate limiter en memoria nunca almacena la IP en texto plano."""
    import hashlib
    from unittest.mock import MagicMock

    from app.services.rate_limit import _fallback_limiters, check_rate_limit

    _fallback_limiters["report"].reset()
    raw_ip = "203.0.113.42"
    request = MagicMock()
    request.headers = {}
    request.client.host = raw_ip

    check_rate_limit(request, scope="report", identifier=raw_ip)

    store = _fallback_limiters["report"]._store
    hashed_ip = hashlib.sha256(raw_ip.encode("utf-8")).hexdigest()
    assert raw_ip not in store
    assert hashed_ip in store


def test_no_metadata_columns_in_report_model():
    from app.models import Report

    forbidden = {"ip_address", "user_agent", "cookies", "device_metadata"}
    columns = {c.name for c in Report.__table__.columns}
    assert forbidden.isdisjoint(columns)


def test_honeypot_rejects_request(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Recibí mensajes inapropiados",
        "honeypot": "spam bot value",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert db_session.query(Report).count() == 0


def test_reported_at_bucket_truncated_to_6h(client, db_session):
    payload = {
        "reported_identifier": "+573001234567",
        "description": "Recibí mensajes inapropiados",
    }
    response = client.post(REPORT_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    report = db_session.query(Report).first()
    assert report.reported_at_bucket is not None
    assert report.reported_at_bucket.minute == 0
    assert report.reported_at_bucket.second == 0
    assert report.reported_at_bucket.microsecond == 0
    assert report.reported_at_bucket.hour % 6 == 0
