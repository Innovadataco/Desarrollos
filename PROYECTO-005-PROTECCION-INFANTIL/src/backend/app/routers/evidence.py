from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AuditLog, Evidence, Report
from app.services.auth import require_role
from app.services.evidence_service import read_evidence_file, save_evidence_file
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/api/v1/reportes", tags=["evidence"])


def _log_audit(db: Session, action: str, actor: str, report_hash: str, details: str):
    log = AuditLog(
        action=action,
        actor_hash=actor,
        report_hash=report_hash,
        details=details,
    )
    db.add(log)
    db.commit()


@router.post("/{report_hash}/evidence")
def upload_evidence(
    request: Request,
    report_hash: str,
    file: UploadFile = File(...),
    description: str | None = None,
    db: Session = Depends(get_db),
):
    """Permite adjuntar archivos a un reporte existente."""
    client_ip = request.client.host if request.client else "anon"
    check_rate_limit(request, scope="report", identifier=client_ip)

    evidence = save_evidence_file(db, report_hash, file, description)
    _log_audit(
        db,
        "evidence_uploaded",
        client_ip,
        report_hash,
        f"kind={evidence.kind}, filename={evidence.original_filename}",
    )
    return {
        "evidence_id": str(evidence.id),
        "report_hash": report_hash,
        "filename": evidence.original_filename,
        "kind": evidence.kind,
        "created_at": evidence.created_at.isoformat() if evidence.created_at else None,
    }


@router.get("/{report_hash}/evidence")
def list_evidence(
    request: Request,
    report_hash: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    evidence_items = db.query(Evidence).filter(Evidence.report_id == report.id).all()
    return [
        {
            "id": str(e.id),
            "kind": e.kind,
            "filename": e.original_filename,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in evidence_items
    ]


@router.get("/{report_hash}/evidence/{evidence_id}")
def download_evidence(
    request: Request,
    report_hash: str,
    evidence_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("viewer")),
):
    check_rate_limit(request, scope="admin", identifier=current_user.username)
    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    import uuid

    try:
        evidence = (
            db.query(Evidence)
            .filter(
                Evidence.id == uuid.UUID(evidence_id), Evidence.report_id == report.id
            )
            .first()
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de evidencia inválido")

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    file_obj, content_type = read_evidence_file(evidence)
    return StreamingResponse(
        file_obj,
        media_type=content_type or "application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={evidence.original_filename or evidence_id}"
        },
    )
