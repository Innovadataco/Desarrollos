from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class EvidenceCreate(BaseModel):
    type: Literal["text", "image", "video", "audio", "screenshot", "url"]
    content: str = Field(..., min_length=1, max_length=50000)


class ReportCreate(BaseModel):
    reported_identifier: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10, max_length=5000)
    category: Literal[
        "contacto_inapropiado",
        "solicitud_material",
        "grooming",
        "cita_persona",
        "extorsion",
        "desconocido",
        "otro",
    ] = "desconocido"
    evidence: EvidenceCreate | None = None
    consent_location: bool = False

    @field_validator("reported_identifier")
    @classmethod
    def strip_identifier(cls, v: str) -> str:
        return v.strip()


class ReportResponse(BaseModel):
    report_hash: str
    reported_at: str
    message: str


class ConsultaRequest(BaseModel):
    identifier: str = Field(..., min_length=1, max_length=255)

    @field_validator("identifier")
    @classmethod
    def strip_identifier(cls, v: str) -> str:
        return v.strip()


class ConsultaResponse(BaseModel):
    identifier_hash: str
    status: Literal["found", "not_found"]
    level: Literal["low", "medium", "high", "critical", "severe"]
    score: float
    report_count: int
    last_reported_at: str | None
    message: str
    resources: list[str] = []
    is_network: bool = False
    severe_report_count: int = 0
    network_geo_countries: int | None = None
    network_geo_cities: int | None = None


class AlertCreate(BaseModel):
    report_hash: str
    level: Literal["low", "medium", "high", "critical", "severe"]
    reason: str = Field(..., min_length=5, max_length=2000)


class AlertUpdate(BaseModel):
    status: Literal["open", "acknowledged", "resolved", "dismissed"] | None = None
    reason: str | None = None
    resolved_by: str | None = None


class AlertResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    report_hash: str | None
    level: str
    reason: str | None
    status: str
    created_at: datetime | None
    updated_at: datetime | None


class ResourceCreate(BaseModel):
    name: str
    url: str
    country: str | None = None
    phone: str | None = None
    description: str | None = None
    priority: int = 100


class ResourceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    name: str
    url: str
    country: str | None
    phone: str | None
    description: str | None
    priority: int


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
    role: Literal["viewer", "supervisor", "admin"]
    email: str | None = None


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    username: str
    email: str | None
    role: str
    is_active: bool
    created_at: str | None


class ReportStatusUpdate(BaseModel):
    status: Literal[
        "received",
        "pending_analysis",
        "analyzed",
        "in_review",
        "escalated",
        "closed",
    ]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GatewayReportRequest(BaseModel):
    report_hash: str
    request_type: Literal["full", "summary"] = "summary"


class GatewayDigestRequest(BaseModel):
    period: Literal["daily", "weekly", "monthly"]
    date: str


class GatewayConfirmRequest(BaseModel):
    report_hash: str
    status: Literal["received", "in_review", "investigating", "closed"]
    notes: str | None = None
