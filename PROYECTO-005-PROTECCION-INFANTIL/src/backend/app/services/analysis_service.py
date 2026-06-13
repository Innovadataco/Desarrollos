import hashlib
from datetime import datetime, timezone

from app.config import settings
from app.models import Analysis, AuditLog, Report
from app.services.encryption import decrypt_field
from app.services.scoring import score_text


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def analyze_report(report: Report, db, actor: str = "system") -> Analysis:
    kek = settings.encryption_kek()
    description = decrypt_field(report.description, kek)

    result = score_text(description)

    analysis = Analysis(
        report_id=report.id,
        score=result["score"],
        level=result["level"],
        category=result["category"],
        category_confidence=result["category_confidence"],
        model_version=result["model_version"],
        grooming_indicators=result["grooming_indicators"],
        explanation=str(result["explanation"]).encode("utf-8"),
        processed_at=datetime.now(timezone.utc),
    )
    db.add(analysis)

    report.score = result["score"]
    report.level = result["level"]
    report.status = "analyzed"
    report.updated_at = datetime.now(timezone.utc)

    audit = AuditLog(
        action="analysis",
        actor_hash=_hash(actor),
        report_hash=report.report_hash,
        details=f"score={result['score']}, level={result['level']}, category={result['category']}",
    )
    db.add(audit)
    db.commit()
    db.refresh(analysis)
    return analysis
