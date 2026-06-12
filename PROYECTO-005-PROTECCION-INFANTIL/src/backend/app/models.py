import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_hash = Column(String(64), unique=True, nullable=False, index=True)
    reported_identifier = Column(LargeBinary, nullable=False)
    description = Column(LargeBinary, nullable=False)
    evidence_type = Column(String(10), nullable=True)
    evidence_content = Column(LargeBinary, nullable=True)
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
