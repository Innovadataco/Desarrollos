"""Gestión segura de archivos de evidencia."""

import io
import logging
import mimetypes
import uuid
from pathlib import Path
from typing import BinaryIO

from fastapi import HTTPException, UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Evidence, Report
from app.services.encryption import decrypt_file, encrypt_file

logger = logging.getLogger(__name__)

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

_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
_UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
_THUMBNAIL_SIZE = (256, 256)


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


def _is_image(extension: str) -> bool:
    return extension.lower() in _IMAGE_EXTENSIONS


def _strip_exif(content: bytes) -> bytes:
    """Elimina metadatos EXIF de imágenes compatibles. Si falla, retorna original."""
    try:
        image = Image.open(io.BytesIO(content))
        # Creamos una copia limpia descartando información EXIF/ICC.
        data = io.BytesIO()
        if image.mode in ("RGBA", "P"):
            image.save(data, format=image.format or "PNG")
        else:
            image.save(data, format=image.format or "JPEG")
        return data.getvalue()
    except Exception as exc:
        logger.warning("No se pudieron eliminar metadatos EXIF: %s", exc)
        return content


def _create_thumbnail(content: bytes, extension: str) -> bytes | None:
    """Genera una miniatura cuadrada para previsualización."""
    try:
        image = Image.open(io.BytesIO(content))
        image.thumbnail(_THUMBNAIL_SIZE)
        fmt = "PNG" if extension.lower() == ".png" else "JPEG"
        data = io.BytesIO()
        image.convert("RGB" if fmt == "JPEG" else None).save(data, format=fmt)
        return data.getvalue()
    except Exception as exc:
        logger.warning("No se pudo generar thumbnail: %s", exc)
        return None


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


def _write_encrypted(path: Path, content: bytes) -> None:
    encrypted = encrypt_file(content, settings.encryption_kek())
    with open(path, "wb") as buffer:
        buffer.write(encrypted)


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

    if _is_image(extension):
        content = _strip_exif(content)

    upload_dir = _ensure_upload_dir()
    safe_name = _sanitize_filename(file.filename or "evidencia")
    stored_name = f"{report_hash}_{uuid.uuid4().hex}{extension}.enc"
    file_path = upload_dir / stored_name
    _write_encrypted(file_path, content)

    thumbnail_path: str | None = None
    if _is_image(extension):
        thumb_content = _create_thumbnail(content, extension)
        if thumb_content:
            thumb_name = f"{report_hash}_{uuid.uuid4().hex}_thumb{extension}.enc"
            thumb_path = upload_dir / thumb_name
            _write_encrypted(thumb_path, thumb_content)
            thumbnail_path = str(thumb_path)

    evidence = Evidence(
        report_id=report.id,
        kind=extension.lstrip("."),
        file_path=str(file_path),
        thumbnail_path=thumbnail_path,
        original_filename=safe_name,
        is_encrypted=True,
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
    content = file_path.read_bytes()
    if evidence.is_encrypted:
        content = decrypt_file(content, settings.encryption_kek())
    content_type = mimetypes.guess_type(evidence.original_filename or file_path.name)[0]
    return io.BytesIO(content), content_type
