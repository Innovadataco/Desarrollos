from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Report
from app.schemas import ConsultaRequest, ConsultaResponse
from app.services.encryption import hash_identifier
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/consultas", tags=["consultas"])


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _log_audit(
    db: Session,
    action: str,
    actor_hash: str,
    report_hash: str | None,
    details: str,
):
    log = AuditLog(
        action=action,
        actor_hash=actor_hash,
        report_hash=report_hash,
        details=details,
    )
    db.add(log)


@router.post("", response_model=ConsultaResponse)
def consulta_semaforo(
    request: Request,
    payload: ConsultaRequest,
    db: Session = Depends(get_db),
):
    actor_hash = hash_identifier(_get_client_ip(request))
    try:
        check_rate_limit(request, scope="consulta", identifier=_get_client_ip(request))
    except HTTPException as exc:
        _log_audit(
            db, "rate_limit", actor_hash, None, f"HTTP {exc.status_code}: {exc.detail}"
        )
        db.commit()
        raise

    identifier_hash = hash_identifier(payload.identifier.strip().lower())
    reports = (
        db.query(Report)
        .filter(Report.identifier_hash == identifier_hash)
        .order_by(Report.reported_at.desc())
        .all()
    )

    if not reports:
        _log_audit(db, "consulta", actor_hash, None, "Sin reportes")
        db.commit()
        return ConsultaResponse(
            identifier_hash=identifier_hash,
            status="not_found",
            level="low",
            score=0.0,
            report_count=0,
            last_reported_at=None,
            message="No encontramos reportes asociados. Mantén la calma y sigue las recomendaciones de seguridad.",
            resources=["https://www.missingkids.org/ES"],
        )

    latest = reports[0]
    level = latest.level or "low"
    score = latest.score or 0.0
    is_network = latest.is_network or False
    severe_report_count = sum(1 for r in reports if r.level in ("severe", "critical"))

    messages = {
        "low": (
            "El nivel de riesgo actual es bajo. No dejes de aplicar medidas básicas de seguridad digital."
        ),
        "medium": (
            "Hay señales de acoso o contacto inapropiado. Revisa la configuración de privacidad "
            "y conversa con una persona de confianza."
        ),
        "high": (
            "El nivel de riesgo es alto. Considera reportar a la plataforma, conservar evidencia y "
            "buscar apoyo de una autoridad o línea de ayuda."
        ),
        "critical": (
            "Riesgo crítico. Si hay grooming, sextorsión o explotación, contacta de inmediato a "
            "la policía o línea nacional de protección infantil."
        ),
        "severe": (
            "Riesgo severo: se detectan indicios graves. Si hay explotación sexual, desaparición o "
            "abuso, llama a emergencias y a tu línea de protección infantil."
        ),
    }

    response = ConsultaResponse(
        identifier_hash=identifier_hash,
        status="found",
        level=level,
        score=round(score, 3),
        report_count=len(reports),
        last_reported_at=latest.reported_at.isoformat() if latest.reported_at else None,
        message=messages.get(level, messages["low"]),
        is_network=is_network,
        severe_report_count=severe_report_count,
        resources=[
            "https://www.missingkids.org/ES",
            "https://www.cybertipline.org/",
        ],
    )

    # If network, also count unique countries/cities.
    if is_network:
        cities = {r.city for r in reports if r.city}
        countries = {r.country for r in reports if r.country}
        response.network_geo_countries = len(countries)
        response.network_geo_cities = len(cities)

    _log_audit(
        db, "consulta", actor_hash, latest.report_hash, f"Nivel {level}, score {score}"
    )
    db.commit()
    return response
