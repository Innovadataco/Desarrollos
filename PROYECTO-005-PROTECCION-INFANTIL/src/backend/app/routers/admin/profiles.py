from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Profile, ProfileUpdate, User
from app.schemas import ProfileResponse
from app.services.auth import require_role
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/profiles", tags=["admin-profiles"])


def _profile_to_dict(profile: Profile) -> dict:
    return {
        "identifier_hash": profile.identifier_hash,
        "identifier_type": profile.identifier_type,
        "report_count": profile.report_count,
        "score_average": profile.score_average,
        "score_max": profile.score_max,
        "score_min": profile.score_min,
        "cities": profile.cities,
        "countries": profile.countries,
        "cities_count": profile.cities_count,
        "countries_count": profile.countries_count,
        "is_network": profile.is_network,
        "evidence_types": profile.evidence_types,
        "categories": profile.categories,
        "first_reported": (
            profile.first_reported.isoformat() if profile.first_reported else None
        ),
        "last_reported": (
            profile.last_reported.isoformat() if profile.last_reported else None
        ),
        "timeline": profile.timeline,
        "alert": (
            f"POSIBLE RED ORGANIZADA: {profile.report_count} reportes desde "
            f"{profile.cities_count} ciudades y {profile.countries_count} países."
            if profile.is_network
            else None
        ),
    }


@router.get("/{identifier_hash}", response_model=ProfileResponse)
def get_profile(
    request: Request,
    identifier_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    profile = (
        db.query(Profile).filter(Profile.identifier_hash == identifier_hash).first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    audit = AuditLog(
        action="view_profile",
        actor_hash=str(current_user.id),
        report_hash=None,
        details=f"profile_hash={identifier_hash}",
    )
    db.add(audit)
    db.commit()
    return ProfileResponse(**_profile_to_dict(profile))


@router.get("/{identifier_hash}/timeline")
def get_timeline(
    request: Request,
    identifier_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    profile = (
        db.query(Profile).filter(Profile.identifier_hash == identifier_hash).first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"identifier_hash": identifier_hash, "timeline": profile.timeline or []}


@router.get("/{identifier_hash}/updates")
def get_updates(
    request: Request,
    identifier_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    profile = (
        db.query(Profile).filter(Profile.identifier_hash == identifier_hash).first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    updates = (
        db.query(ProfileUpdate)
        .filter(ProfileUpdate.profile_id == profile.id)
        .order_by(ProfileUpdate.created_at.desc())
        .all()
    )
    return {
        "identifier_hash": identifier_hash,
        "updates": [
            {
                "id": str(u.id),
                "old_score_avg": u.old_score_avg,
                "new_score_avg": u.new_score_avg,
                "old_cities_count": u.old_cities_count,
                "new_cities_count": u.new_cities_count,
                "old_countries_count": u.old_countries_count,
                "new_countries_count": u.new_countries_count,
                "old_is_network": u.old_is_network,
                "new_is_network": u.new_is_network,
                "triggered_network": u.triggered_network,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in updates
        ],
    }


@router.get("/networks/list")
def list_networks(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    profiles = (
        db.query(Profile)
        .filter(Profile.is_network.is_(True))
        .order_by(Profile.updated_at.desc())
        .all()
    )
    return [_profile_to_dict(p) for p in profiles]
