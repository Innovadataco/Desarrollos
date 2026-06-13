import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("ix_reports_identifier_reported_at", "identifier_hash", "reported_at"),
        Index("ix_reports_level_status", "level", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_hash = Column(String(64), unique=True, nullable=False, index=True)
    reported_identifier = Column(LargeBinary, nullable=False)
    description = Column(LargeBinary, nullable=False)
    category = Column(String(20), nullable=False, default="desconocido")
    evidence_type = Column(String(20), nullable=True)
    evidence_content = Column(LargeBinary, nullable=True)
    identifier_hash = Column(String(64), nullable=False, index=True)
    identifier_type = Column(String(20), nullable=False, default="text")
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    consent_location = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default="received")
    score = Column(Float, nullable=True)
    level = Column(String(20), nullable=True)
    is_network = Column(Boolean, nullable=False, default=False)
    reported_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    analyses = relationship(
        "Analysis", back_populates="report", cascade="all, delete-orphan"
    )
    alerts = relationship(
        "Alert", back_populates="report", cascade="all, delete-orphan"
    )
    evidences = relationship(
        "Evidence", back_populates="report", cascade="all, delete-orphan"
    )


class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    kind = Column(String(20), nullable=False)
    content = Column(LargeBinary, nullable=True)
    file_path = Column(String(255), nullable=True)
    original_filename = Column(String(255), nullable=True)
    source = Column(String(20), nullable=False, default="user_upload")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    report = relationship("Report", back_populates="evidences")


class Identifier(Base):
    __tablename__ = "identifiers"
    __table_args__ = (UniqueConstraint("hash"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String(64), nullable=False, unique=True, index=True)
    type = Column(String(20), nullable=False, default="text")
    report_count = Column(Integer, nullable=False, default=0)
    first_seen = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    score = Column(Float, nullable=False)
    level = Column(String(20), nullable=False)
    category = Column(String(20), nullable=False)
    category_confidence = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    explanation = Column(LargeBinary, nullable=True)
    grooming_indicators = Column(JSON, nullable=True)
    processed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    report = relationship("Report", back_populates="analyses")


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = (UniqueConstraint("identifier_hash"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier_hash = Column(String(64), nullable=False, unique=True, index=True)
    identifier_type = Column(String(20), nullable=False)
    report_count = Column(Integer, nullable=False, default=0)
    score_average = Column(Float, nullable=True)
    score_max = Column(Float, nullable=True)
    score_min = Column(Float, nullable=True)
    cities = Column(JSON, nullable=True)
    countries = Column(JSON, nullable=True)
    cities_count = Column(Integer, nullable=False, default=0)
    countries_count = Column(Integer, nullable=False, default=0)
    is_network = Column(Boolean, nullable=False, default=False)
    evidence_types = Column(JSON, nullable=True)
    categories = Column(JSON, nullable=True)
    first_reported = Column(DateTime(timezone=True), nullable=True)
    last_reported = Column(DateTime(timezone=True), nullable=True)
    network_countries = Column(JSON, nullable=True)
    related_profiles = Column(JSON, nullable=True)
    timeline = Column(JSON, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class ProfileUpdate(Base):
    __tablename__ = "profile_updates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    report_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=True
    )
    old_score_avg = Column(Float, nullable=True)
    new_score_avg = Column(Float, nullable=True)
    old_cities_count = Column(Integer, nullable=True)
    new_cities_count = Column(Integer, nullable=True)
    old_countries_count = Column(Integer, nullable=True)
    new_countries_count = Column(Integer, nullable=True)
    old_is_network = Column(Boolean, nullable=True)
    new_is_network = Column(Boolean, nullable=True)
    triggered_network = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="viewer")
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    totp_secret = Column(String(255), nullable=True)
    totp_enabled = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_action_created", "action", "created_at"),
        Index("ix_audit_logs_report_hash", "report_hash"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String(50), nullable=False)
    actor_hash = Column(String(64), nullable=True)
    report_hash = Column(String(64), nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Institution(Base):
    __tablename__ = "institutions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    contact_person = Column(String(100), nullable=True)
    contract_active = Column(Boolean, nullable=False, default=False)
    contract_signed_at = Column(Date, nullable=True)
    contract_expires_at = Column(Date, nullable=True)
    alert_config = Column(JSON, nullable=False, default=dict)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_hash = Column(String(64), nullable=True, index=True)
    report_id = Column(
        UUID(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=True
    )
    level = Column(String(20), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="open")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    report = relationship("Report", back_populates="alerts")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=100)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SystemConfig(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, default=1)
    threshold_severe = Column(Float, nullable=False, default=0.85)
    threshold_critical = Column(Float, nullable=False, default=0.70)
    threshold_high = Column(Float, nullable=False, default=0.50)
    threshold_medium = Column(Float, nullable=False, default=0.30)
    alert_severe_immediate = Column(Boolean, nullable=False, default=True)
    alert_critical_4h = Column(Boolean, nullable=False, default=True)
    alert_high_24h = Column(Boolean, nullable=False, default=True)
    alert_medium_weekly = Column(Boolean, nullable=False, default=True)
    alert_network_immediate = Column(Boolean, nullable=False, default=True)
    digest_daily_time = Column(String(5), nullable=False, default="08:00")
    digest_weekly_day = Column(Integer, nullable=False, default=1)
    digest_weekly_time = Column(String(5), nullable=False, default="08:00")
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_by = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
