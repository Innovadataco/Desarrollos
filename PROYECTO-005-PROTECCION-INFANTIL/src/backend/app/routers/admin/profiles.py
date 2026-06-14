from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Profile, ProfileUpdate, User
from app.schemas import ProfileResponse
from app.services import cache_service
from app.services.auth import require_role
from app.services.profile_service import profile_to_dict
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/profiles", tags=["admin-profiles"])


@router.get("", response_model=list[ProfileResponse])
def list_profiles(
    request: Request,
    report_count_min: int | None = Query(None, ge=0),
    score_min: float | None = Query(None, ge=0.0, le=1.0),
    is_network: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    query = db.query(Profile)
    if report_count_min is not None:
        query = query.filter(Profile.report_count >= report_count_min)
    if score_min is not None:
        query = query.filter(Profile.score_average >= score_min)
    if is_network is not None:
        query = query.filter(Profile.is_network.is_(is_network))

    profiles = query.order_by(Profile.updated_at.desc()).all()
    return [profile_to_dict(p) for p in profiles]


@router.get("/networks/list", response_model=list[ProfileResponse])
def list_networks(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)

    cache_key = "networks:list"
    cached = cache_service.get_key(cache_key)
    if cached:
        return [ProfileResponse(**item) for item in cached]

    profiles = (
        db.query(Profile)
        .filter(Profile.is_network.is_(True))
        .order_by(Profile.updated_at.desc())
        .all()
    )
    data = [profile_to_dict(p) for p in profiles]
    cache_service.set_key(cache_key, data, ttl_seconds=900)
    return [ProfileResponse(**item) for item in data]


@router.get("/{identifier_hash}", response_model=ProfileResponse)
def get_profile(
    request: Request,
    identifier_hash: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)

    cache_key = f"profile:{identifier_hash}"
    cached = cache_service.get_key(cache_key)
    if cached:
        audit = AuditLog(
            action="view_profile",
            actor_hash=str(current_user.id),
            report_hash=None,
            details=f"profile_hash={identifier_hash} (cache)",
        )
        db.add(audit)
        db.commit()
        return ProfileResponse(**cached)

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

    data = profile_to_dict(profile)
    cache_service.set_key(cache_key, data, ttl_seconds=3600)
    return ProfileResponse(**data)


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
