"""Gestión segura de archivos de evidencia."""

import mimetypes
import shutil
import uuid
from pathlib import Path
from typing import BinaryIO

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models import Evidence, Report

_ALLOWED_MIME_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "application/pdf": ".pdf",
    "text/plain": ".txt",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/webm": ".webm",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
}

_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
_UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"


def _ensure_upload_dir() -> Path:
    _UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return _UPLOAD_DIR


def _sanitize_filename(filename: str) -> str:
    """Conserva solo el nombre base, sin path traversal."""
    import os
    import re

    name = os.path.basename(filename)
    name = re.sub(r"[^\w\s.-]", "", name)
    return name.strip() or "evidencia"


def validate_upload(file: UploadFile) -> tuple[str, str]:
    content_type = file.content_type or "application/octet-stream"
    extension = _ALLOWED_MIME_EXTENSIONS.get(content_type)
    if not extension:
        # Fallback: intentar deducir por nombre si el MIME no está mapeado
        guessed = mimetypes.guess_type(file.filename or "")[0]
        extension = _ALLOWED_MIME_EXTENSIONS.get(guessed) if guessed else None
    if not extension:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {content_type}",
        )
    return content_type, extension


def save_evidence_file(
    db: Session,
    report_hash: str,
    file: UploadFile,
    description: str | None = None,
) -> Evidence:
    report = db.query(Report).filter(Report.report_hash == report_hash).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    content_type, extension = validate_upload(file)

    # Leer contenido para validar tamaño.
    content = file.file.read(_MAX_FILE_SIZE_BYTES + 1)
    if len(content) > _MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Archivo demasiado grande. Máximo {_MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB.",
        )

    upload_dir = _ensure_upload_dir()
    safe_name = _sanitize_filename(file.filename or "evidencia")
    # Evitar colisiones: hash aleatorio + extensión confiable.
    stored_name = f"{report_hash}_{uuid.uuid4().hex}{extension}"
    file_path = upload_dir / stored_name

    with open(file_path, "wb") as buffer:
        buffer.write(content)
        # Si el archivo es mayor al chunk leído (no debería tras validación),
        # copiar el resto.
        shutil.copyfileobj(file.file, buffer)

    evidence = Evidence(
        report_id=report.id,
        kind=extension.lstrip("."),
        file_path=str(file_path),
        original_filename=safe_name,
        source="user_upload",
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


def read_evidence_file(evidence: Evidence) -> tuple[BinaryIO, str | None]:
    if not evidence.file_path or not Path(evidence.file_path).exists():
        raise HTTPException(
            status_code=404, detail="Archivo de evidencia no encontrado"
        )
    file_path = Path(evidence.file_path)
    content_type = mimetypes.guess_type(file_path.name)[0]
    return open(file_path, "rb"), content_type
