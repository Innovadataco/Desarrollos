from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resource
from app.schemas import ResourceCreate, ResourceResponse
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.get("", response_model=list[ResourceResponse])
def list_resources(
    request: Request,
    country: str | None = None,
    db: Session = Depends(get_db),
):
    check_rate_limit(
        request,
        scope="resource",
        identifier=request.client.host if request.client else "anon",
    )
    query = db.query(Resource)
    if country:
        query = query.filter(Resource.country == country)
    return query.order_by(Resource.priority.asc()).all()


@router.post("", response_model=ResourceResponse, status_code=201)
def create_resource(
    request: Request,
    payload: ResourceCreate,
    db: Session = Depends(get_db),
):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource
