"""Envío de alertas y digest por correo a instituciones."""

from datetime import datetime
from email.message import EmailMessage

import aiosmtplib
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Alert, Institution, Report


def _smtp_configured() -> bool:
    return bool(settings.smtp_host and settings.smtp_user and settings.smtp_password)


async def send_email(to: str, subject: str, body: str) -> dict:
    if not _smtp_configured():
        return {"sent": False, "reason": "SMTP no configurado"}

    message = EmailMessage()
    message["From"] = settings.smtp_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            start_tls=settings.smtp_tls,
        )
        return {"sent": True}
    except Exception as exc:
        return {"sent": False, "reason": str(exc)}


def build_alert_body(alert: Alert, report: Report | None) -> str:
    lines = [
        "Alerta automática - Semáforo de Confianza",
        "",
        f"Nivel: {alert.level}",
        f"Reporte: {alert.report_hash or 'N/A'}",
        f"Razón: {alert.reason or 'N/A'}",
        f"Generada: {alert.created_at.isoformat() if alert.created_at else 'N/A'}",
    ]
    if report:
        lines.extend(
            [
                "",
                f"Score IA: {report.score}",
                f"Categoría: {report.category}",
                f"Ubicación: {report.city or ''}, {report.country or ''}",
            ]
        )
    return "\n".join(lines)


def build_digest_body(institution: Institution, counts: dict, since: datetime) -> str:
    return (
        f"Digest {institution.name} - {since.date().isoformat()}\n\n"
        f"Reportes nuevos: {counts['total']}\n"
        f"Severe: {counts['severe']}\n"
        f"Critical: {counts['critical']}\n"
        f"High: {counts['high']}\n"
        f"Medium: {counts['medium']}\n"
        f"Low: {counts['low']}\n"
        f"Redes detectadas: {counts['network']}\n"
    )


async def send_alert_to_institution(db: Session, alert: Alert) -> dict:
    report = None
    if alert.report_id:
        report = db.query(Report).filter(Report.id == alert.report_id).first()

    subject = f"[Alerta {alert.level.upper()}] Semáforo de Confianza"
    body = build_alert_body(alert, report)
    results = []
    for inst in (
        db.query(Institution).filter(Institution.contract_active.is_(True)).all()
    ):
        result = await send_email(inst.contact_email, subject, body)
        results.append({"institution": inst.code, **result})
    return {"alert_id": str(alert.id), "recipients": results}


async def send_digest_to_institution(
    db: Session, institution: Institution, since: datetime
) -> dict:
    reports = db.query(Report).filter(Report.reported_at >= since).all()
    counts = {
        "total": len(reports),
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
    subject = f"Digest diario - {institution.name}"
    body = build_digest_body(institution, counts, since)
    result = await send_email(institution.contact_email, subject, body)
    return {"institution": institution.code, **result}
