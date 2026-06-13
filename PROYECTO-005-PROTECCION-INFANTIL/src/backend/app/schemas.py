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
        "CAT-01",
        "CAT-02",
        "CAT-03",
        "CAT-04",
        "CAT-05",
        "CAT-06",
    ] = "CAT-06"
    evidence: EvidenceCreate | None = None
    evidence_media_url: str | None = Field(default=None, max_length=500)
    consent_location: bool = False
    honeypot: str | None = Field(default=None, max_length=255)

    @field_validator("reported_identifier")
    @classmethod
    def strip_identifier(cls, v: str) -> str:
        return v.strip()


class ReportResponse(BaseModel):
    report_hash: str
    reported_at: str
    reported_at_bucket: str | None = None
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


class SemaforoResponse(BaseModel):
    identifier_hash: str
    semaforo: Literal["verde", "amarillo", "rojo", "negro"]
    report_count: int
    score_average: float | None
    score_max: float | None
    first_reported_at: str | None
    last_reported_at: str | None
    categories: list[str] | None
    cities_count: int
    countries_count: int
    is_network: bool
    message: str
    report_button: bool = True


class AnalysisResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    report_id: UUID
    score: float
    level: str
    category: str
    category_confidence: float
    model_version: str
    grooming_indicators: list[str] | None = None
    explanation: str | None = None
    processed_at: datetime | None = None
    created_at: datetime | None = None


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
    notes: str | None = None


class AdminReportListItem(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    report_hash: str
    reported_at: datetime | None
    score: float | None
    level: str | None
    category: str
    status: str
    city: str | None
    country: str | None
    evidence_type: str | None
    has_evidence: bool = False


class AdminReportDetail(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    report_hash: str
    reported_at: datetime | None
    updated_at: datetime | None
    score: float | None
    level: str | None
    category: str
    status: str
    city: str | None
    country: str | None
    evidence_type: str | None
    identifier_type: str
    identifier_hash: str
    has_evidence: bool = False


class DecryptRequest(BaseModel):
    reason: str = Field(..., min_length=20)


class DecryptResponse(BaseModel):
    decrypted_at: str
    reported_identifier: str
    description: str
    evidence_content: str | None
    evidence_type: str | None
    audit_log_id: str | None


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


class ProfileResponse(BaseModel):
    identifier_hash: str
    identifier_type: str
    report_count: int
    score_average: float | None
    score_max: float | None
    score_min: float | None
    cities: list[str]
    countries: list[str]
    cities_count: int
    countries_count: int
    is_network: bool
    evidence_types: list[str]
    categories: list[str]
    first_reported: str | None
    last_reported: str | None
    timeline: list[dict] | None
    alert: str | None


class AuditLogItem(BaseModel):
    id: str
    action: str
    actor_hash: str | None
    report_hash: str | None
    details: str | None
    created_at: str | None


class AuditLogListResponse(BaseModel):
    total: int
    page: int
    limit: int
    logs: list[AuditLogItem]


class NCMECExportRequest(BaseModel):
    report_hash: str


class NCMECExportResponse(BaseModel):
    format: str = "ncmec-like"
    report_hash: str
    incident_type: str
    reporting_person: dict
    subject: dict
    incident_summary: str
    identifiers: list[dict]
    risk_score: float | None
    risk_level: str | None
    generated_at: str
