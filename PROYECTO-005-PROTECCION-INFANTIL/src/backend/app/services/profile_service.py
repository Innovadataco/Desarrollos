from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models import Profile, ProfileUpdate, Report
from app.services import cache_service


def _month_key(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def _detect_network(profile: Profile) -> tuple[bool, list[str]]:
    criteria = []
    if profile.cities_count and profile.cities_count >= 3:
        criteria.append("cities>=3")
    if profile.countries_count and profile.countries_count >= 2:
        criteria.append("countries>=2")
    if (
        profile.report_count
        and profile.report_count >= 5
        and profile.score_average
        and profile.score_average > 0.6
    ):
        criteria.append("reports>=5_avg>0.6")
    evidence_types = profile.evidence_types or []
    if len(evidence_types) >= 3:
        criteria.append("evidence_types>=3")
    return len(criteria) >= 2, criteria


def profile_to_dict(profile: Profile) -> dict[str, Any]:
    """Serializa un Profile para respuestas de API y cache."""
    return {
        "identifier_hash": profile.identifier_hash,
        "identifier_type": profile.identifier_type,
        "report_count": profile.report_count,
        "score_average": profile.score_average,
        "score_max": profile.score_max,
        "score_min": profile.score_min,
        "cities": profile.cities or [],
        "countries": profile.countries or [],
        "cities_count": profile.cities_count,
        "countries_count": profile.countries_count,
        "is_network": profile.is_network,
        "evidence_types": profile.evidence_types or [],
        "categories": profile.categories or [],
        "first_reported": (
            profile.first_reported.isoformat() if profile.first_reported else None
        ),
        "last_reported": (
            profile.last_reported.isoformat() if profile.last_reported else None
        ),
        "timeline": profile.timeline or [],
        "alert": (
            f"POSIBLE RED ORGANIZADA: {profile.report_count} reportes desde "
            f"{profile.cities_count} ciudades y {profile.countries_count} países."
            if profile.is_network
            else None
        ),
    }


def update_profile_from_report(report: Report, db: Session) -> Profile:
    profile = (
        db.query(Profile)
        .filter(Profile.identifier_hash == report.identifier_hash)
        .first()
    )
    old_score_avg = profile.score_average if profile else None
    old_cities_count = profile.cities_count if profile else 0
    old_countries_count = profile.countries_count if profile else 0
    old_is_network = profile.is_network if profile else False

    if not profile:
        profile = Profile(
            identifier_hash=report.identifier_hash,
            identifier_type=report.identifier_type,
            report_count=0,
            cities_count=0,
            countries_count=0,
            is_network=False,
            cities=[],
            countries=[],
            evidence_types=[],
            categories=[],
            timeline=[],
        )
        db.add(profile)
        db.flush()

    reports = (
        db.query(Report)
        .filter(Report.identifier_hash == report.identifier_hash)
        .order_by(Report.reported_at.asc())
        .all()
    )

    cities = sorted({r.city for r in reports if r.city})
    countries = sorted({r.country for r in reports if r.country})
    categories = sorted({r.category for r in reports if r.category})
    evidence_types = sorted({r.evidence_type for r in reports if r.evidence_type})

    scores = [r.score for r in reports if r.score is not None]
    score_avg = sum(scores) / len(scores) if scores else None
    score_max = max(scores) if scores else None
    score_min = min(scores) if scores else None

    timeline_map: dict[str, dict[str, Any]] = {}
    for r in reports:
        key = _month_key(r.reported_at)
        entry = timeline_map.setdefault(
            key, {"month": key, "count": 0, "score_avg": 0.0}
        )
        entry["count"] += 1
        entry["score_avg"] += r.score or 0.0
    timeline = []
    for key in sorted(timeline_map):
        entry = timeline_map[key]
        if entry["count"]:
            entry["score_avg"] = round(entry["score_avg"] / entry["count"], 3)
        timeline.append(entry)

    profile.report_count = len(reports)
    profile.score_average = round(score_avg, 3) if score_avg is not None else None
    profile.score_max = round(score_max, 3) if score_max is not None else None
    profile.score_min = round(score_min, 3) if score_min is not None else None
    profile.cities = cities
    profile.countries = countries
    profile.cities_count = len(cities)
    profile.countries_count = len(countries)
    profile.evidence_types = evidence_types
    profile.categories = categories
    profile.first_reported = reports[0].reported_at if reports else None
    profile.last_reported = reports[-1].reported_at if reports else None
    profile.timeline = timeline
    profile.updated_at = datetime.now(timezone.utc)

    is_network, criteria = _detect_network(profile)
    profile.is_network = is_network
    profile.network_countries = countries if is_network else None
    profile.related_profiles = criteria if is_network else None

    db.flush()

    update = ProfileUpdate(
        profile_id=profile.id,
        report_id=report.id,
        old_score_avg=old_score_avg,
        new_score_avg=profile.score_average,
        old_cities_count=old_cities_count,
        new_cities_count=profile.cities_count,
        old_countries_count=old_countries_count,
        new_countries_count=profile.countries_count,
        old_is_network=old_is_network,
        new_is_network=profile.is_network,
        triggered_network=(not old_is_network and profile.is_network),
        created_at=datetime.now(timezone.utc),
    )
    db.add(update)
    db.commit()
    db.refresh(profile)

    # Cache del perfil (TTL 1h) e invalidación de la lista de redes.
    cache_service.set_key(
        f"profile:{profile.identifier_hash}", profile_to_dict(profile), ttl_seconds=3600
    )
    cache_service.delete_key("networks:list")

    return profile
