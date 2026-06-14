"""Exportación segura de reportes en JSON y PDF."""

from datetime import datetime, timezone
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy.orm import Session

from app.models import AuditLog, Report
from app.services.encryption import decrypt_field
from app.config import settings


def export_report_json(report: Report, include_encrypted: bool = False) -> dict:
    """Exporta un reporte como diccionario JSON."""
    data = {
        "report_hash": report.report_hash,
        "identifier_hash": report.identifier_hash,
        "identifier_type": report.identifier_type,
        "category": report.category,
        "level": report.level,
        "score": report.score,
        "status": report.status,
        "city": report.city,
        "country": report.country,
        "consent_location": report.consent_location,
        "reported_at": report.reported_at.isoformat() if report.reported_at else None,
        "updated_at": report.updated_at.isoformat() if report.updated_at else None,
        "evidence_type": report.evidence_type,
        "is_network": report.is_network,
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }
    if include_encrypted:
        kek = settings.encryption_kek()
        data["reported_identifier"] = decrypt_field(report.reported_identifier, kek)
        data["description"] = decrypt_field(report.description, kek)
        if report.evidence_content:
            data["evidence_content"] = decrypt_field(report.evidence_content, kek)
        else:
            data["evidence_content"] = None
    return data


def _safe(value: str | None) -> str:
    return value or "N/A"


def export_report_pdf(report: Report, include_encrypted: bool = False) -> bytes:
    """Genera un PDF en memoria con los datos del reporte."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("<b>Reporte Semáforo de Confianza</b>", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))

    sensitive_rows = []
    if include_encrypted:
        kek = settings.encryption_kek()
        sensitive_rows = [
            [
                "Identificador reportado",
                _safe(decrypt_field(report.reported_identifier, kek)),
            ],
            ["Descripción", _safe(decrypt_field(report.description, kek))],
        ]
        if report.evidence_content:
            sensitive_rows.append(
                ["Evidencia", _safe(decrypt_field(report.evidence_content, kek))]
            )

    rows = [
        ["Hash de reporte", _safe(report.report_hash)],
        ["Hash de identificador", _safe(report.identifier_hash)],
        ["Tipo de identificador", _safe(report.identifier_type)],
        ["Categoría", _safe(report.category)],
        ["Nivel de riesgo", _safe(report.level)],
        ["Score", str(report.score) if report.score is not None else "N/A"],
        ["Estado", _safe(report.status)],
        ["Ciudad", _safe(report.city)],
        ["País", _safe(report.country)],
        ["Consentimiento ubicación", "Sí" if report.consent_location else "No"],
        ["Reportado", report.reported_at.isoformat() if report.reported_at else "N/A"],
        ["Actualizado", report.updated_at.isoformat() if report.updated_at else "N/A"],
        ["Tipo de evidencia", _safe(report.evidence_type)],
        ["Red organizada", "Sí" if report.is_network else "No"],
    ] + sensitive_rows

    table = Table(rows, colWidths=[180, 320])
    table.setStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
    )
    story.append(table)
    story.append(Spacer(1, 12))

    if include_encrypted:
        story.append(
            Paragraph(
                "<font size=8 color=red>Este documento contiene datos personales desencriptados.</font>",
                styles["Normal"],
            )
        )

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def list_audit_logs(
    db: Session,
    report_hash: str | None = None,
    action: str | None = None,
    page: int = 1,
    limit: int = 50,
) -> dict:
    query = db.query(AuditLog)
    if report_hash:
        query = query.filter(AuditLog.report_hash == report_hash)
    if action:
        query = query.filter(AuditLog.action == action)
    total = query.count()
    logs = (
        query.order_by(AuditLog.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "logs": [
            {
                "id": str(log.id),
                "action": log.action,
                "actor_hash": log.actor_hash,
                "report_hash": log.report_hash,
                "details": log.details,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
    }
