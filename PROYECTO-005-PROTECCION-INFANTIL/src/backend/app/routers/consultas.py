from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Report
from app.schemas import ConsultaRequest, SemaforoResponse
from app.services.cache_service import get as get_cache, set as set_cache
from app.services.identifier import hash_identifier, normalize_identifier
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1", tags=["consultas"])


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


def _calculate_semaphore(
    report_count: int,
    score_max: float | None,
    cities_count: int,
    countries_count: int,
) -> tuple[str, bool]:
    is_network = cities_count >= 3 or countries_count >= 2
    if is_network:
        return "negro", is_network
    if report_count >= 3 or (score_max is not None and score_max >= 0.8):
        return "rojo", is_network
    if report_count >= 1 or (score_max is not None and score_max >= 0.5):
        return "amarillo", is_network
    return "verde", is_network


def _build_result(identifier_hash: str, reports: list[Report]) -> SemaforoResponse:
    if not reports:
        return SemaforoResponse(
            identifier_hash=identifier_hash,
            semaforo="verde",
            report_count=0,
            score_average=None,
            score_max=None,
            first_reported_at=None,
            last_reported_at=None,
            categories=None,
            cities_count=0,
            countries_count=0,
            is_network=False,
            message="Sin reportes registrados. El semáforo está verde.",
            report_button=True,
        )

    scores = [r.score for r in reports if r.score is not None]
    score_avg = sum(scores) / len(scores) if scores else None
    score_max = max(scores) if scores else None

    cities = {r.city for r in reports if r.city}
    countries = {r.country for r in reports if r.country}
    categories = list({r.category for r in reports if r.category})

    semaforo, is_network = _calculate_semaphore(
        len(reports), score_max, len(cities), len(countries)
    )

    first_reported = reports[-1].reported_at.date().isoformat()
    last_reported = reports[0].reported_at.date().isoformat()

    if semaforo == "negro":
        message = (
            f"Este identificador tiene {len(reports)} reportes desde "
            f"{len(cities)} ciudades y {len(countries)} países. Posible red organizada."
        )
    elif semaforo == "rojo":
        message = (
            f"Este identificador tiene {len(reports)} reportes de contacto inapropiado "
            "con menores. Se recomienda reportar o consultar autoridades."
        )
    elif semaforo == "amarillo":
        message = (
            f"Este identificador tiene {len(reports)} reporte(s) previo(s). "
            "Mantén la precaución."
        )
    else:
        message = "Sin reportes registrados. El semáforo está verde."

    return SemaforoResponse(
        identifier_hash=identifier_hash,
        semaforo=semaforo,
        report_count=len(reports),
        score_average=round(score_avg, 3) if score_avg is not None else None,
        score_max=round(score_max, 3) if score_max is not None else None,
        first_reported_at=first_reported,
        last_reported_at=last_reported,
        categories=categories,
        cities_count=len(cities),
        countries_count=len(countries),
        is_network=is_network,
        message=message,
        report_button=True,
    )


def _query_reports(db: Session, identifier_hash: str) -> list[Report]:
    return (
        db.query(Report)
        .filter(Report.identifier_hash == identifier_hash)
        .order_by(Report.reported_at.desc())
        .all()
    )


@router.post("/consultas", response_model=SemaforoResponse)
def consulta_semaforo(
    request: Request,
    payload: ConsultaRequest,
    db: Session = Depends(get_db),
):
    actor_hash = hash_identifier(_get_client_ip(request))
    try:
        check_rate_limit(request, scope="validate", identifier=_get_client_ip(request))
    except HTTPException as exc:
        detail = exc.detail.get("error") if isinstance(exc.detail, dict) else exc.detail
        _log_audit(
            db, "rate_limit", actor_hash, None, f"HTTP {exc.status_code}: {detail}"
        )
        db.commit()
        raise

    identifier_type, _ = normalize_identifier(payload.identifier)
    identifier_hash = hash_identifier(payload.identifier)

    cached = get_cache(identifier_hash)
    if cached:
        _log_audit(
            db,
            "consulta_cache",
            actor_hash,
            None,
            f"Tipo {identifier_type}, cache hit",
        )
        db.commit()
        return SemaforoResponse(**cached)

    reports = _query_reports(db, identifier_hash)
    result = _build_result(identifier_hash, reports)

    set_cache(identifier_hash, result.model_dump(mode="json"), ttl_seconds=3600)

    _log_audit(
        db,
        "consulta",
        actor_hash,
        reports[0].report_hash if reports else None,
        f"Tipo {identifier_type}, semaforo {result.semaforo}, reportes {result.report_count}",
    )
    db.commit()
    return result


@router.get("/validate/{identifier}", response_model=SemaforoResponse)
def validate_identifier(
    request: Request,
    identifier: str,
    db: Session = Depends(get_db),
):
    return consulta_semaforo(request, ConsultaRequest(identifier=identifier), db)
