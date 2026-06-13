from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Institution, Profile, Report
from app.schemas import (
    GatewayConfirmRequest,
    GatewayDigestRequest,
    GatewayReportRequest,
)
from app.services.auth import verify_password
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/gateway", tags=["gateway"])


def get_institution(request: Request, db: Session) -> Institution:
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key requerida")
    institutions = db.query(Institution).all()
    for inst in institutions:
        if inst.api_key_hash and verify_password(api_key, inst.api_key_hash):
            return inst
    raise HTTPException(status_code=401, detail="API key inválida")


def _profile_to_dict(profile: Profile | None) -> dict | None:
    if not profile:
        return None
    return {
        "id": str(profile.id),
        "identifier_hash": profile.identifier_hash,
        "identifier_type": profile.identifier_type,
        "report_count": profile.report_count,
        "first_reported": (
            profile.first_reported.isoformat() if profile.first_reported else None
        ),
        "last_reported": (
            profile.last_reported.isoformat() if profile.last_reported else None
        ),
        "risk_level": (
            "severe"
            if profile.score_average and profile.score_average >= 0.85
            else (
                "critical"
                if profile.score_average and profile.score_average >= 0.7
                else (
                    "high"
                    if profile.score_average and profile.score_average >= 0.5
                    else (
                        "medium"
                        if profile.score_average and profile.score_average >= 0.3
                        else "low"
                    )
                )
            )
        ),
        "score": profile.score_average,
        "score_max": profile.score_max,
        "is_network": profile.is_network,
        "network_countries": profile.network_countries or [],
        "related_profiles": profile.related_profiles or [],
    }


@router.post("/reports")
def gateway_report(
    request: Request,
    payload: GatewayReportRequest,
    db: Session = Depends(get_db),
):
    institution = get_institution(request, db)
    check_rate_limit(request, scope="gateway", identifier=institution.code)

    report = db.query(Report).filter(Report.report_hash == payload.report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    profile = (
        db.query(Profile)
        .filter(Profile.identifier_hash == report.identifier_hash)
        .first()
    )
    profile_dict = _profile_to_dict(profile)

    if payload.request_type == "full":
        return {
            "report_hash": report.report_hash,
            "identifier_hash": report.identifier_hash,
            "identifier_type": report.identifier_type,
            "category": report.category,
            "level": report.level,
            "score": report.score,
            "status": report.status,
            "reported_at": (
                report.reported_at.isoformat() if report.reported_at else None
            ),
            "city": report.city,
            "country": report.country,
            "evidence_type": report.evidence_type,
            "profile": profile_dict,
        }

    return {
        "report_hash": report.report_hash,
        "category": report.category,
        "score": report.score,
        "level": report.level,
        "reported_at": report.reported_at.isoformat() if report.reported_at else None,
        "identifier_type": report.identifier_type,
        "identifier_hash": report.identifier_hash,
        "evidence_types": [report.evidence_type] if report.evidence_type else [],
    }


@router.post("/digest")
def gateway_digest(
    request: Request,
    payload: GatewayDigestRequest,
    db: Session = Depends(get_db),
):
    institution = get_institution(request, db)
    check_rate_limit(request, scope="gateway", identifier=institution.code)

    today = datetime.now(timezone.utc).date()
    today_start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    reports = db.query(Report).filter(Report.reported_at >= today_start).all()
    counts = {
        "severe": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "network": 0,
    }
    for r in reports:
        if r.level in counts:
            counts[r.level] += 1
        if r.is_network:
            counts["network"] += 1

    return {
        "period": payload.period,
        "date": payload.date,
        "report_count": len(reports),
        "severe_count": counts["severe"],
        "critical_count": counts["critical"],
        "high_count": counts["high"],
        "medium_count": counts["medium"],
        "low_count": counts["low"],
        "network_count": counts["network"],
        "reports": [],
    }


@router.post("/confirm")
def gateway_confirm(
    request: Request,
    payload: GatewayConfirmRequest,
    db: Session = Depends(get_db),
):
    institution = get_institution(request, db)
    check_rate_limit(request, scope="gateway", identifier=institution.code)

    report = db.query(Report).filter(Report.report_hash == payload.report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    return {
        "confirmed": True,
        "report_hash": report.report_hash,
        "status": payload.status,
        "confirmed_at": datetime.now(timezone.utc).isoformat(),
    }
