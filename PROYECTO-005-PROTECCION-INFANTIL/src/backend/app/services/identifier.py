import hashlib
import re
from urllib.parse import urlparse


def detect_identifier_type(value: str) -> str:
    cleaned = value.strip()
    if re.fullmatch(r"\+?\d[\d\s\-\(\)]{6,20}", cleaned):
        return "phone"
    if re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", cleaned):
        return "email"
    if cleaned.startswith("@"):
        return "social"
    if cleaned.lower().startswith(("http://", "https://")):
        return "url"
    return "text"


def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    # E.164 mínimo: código de país + número. Si no tiene +, dejar digits.
    if value.strip().startswith("+"):
        return f"+{digits}"
    return digits


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_social(value: str) -> str:
    return value.strip().lstrip("@").lower()


def normalize_url(value: str) -> str:
    url = value.strip().lower()
    parsed = urlparse(url)
    netloc = parsed.netloc or parsed.path.split("/")[0]
    netloc = netloc.removeprefix("www.")
    path = parsed.path.rstrip("/")
    return f"{netloc}{path}"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().lower())


def normalize_identifier(value: str) -> tuple[str, str]:
    identifier_type = detect_identifier_type(value)
    if identifier_type == "phone":
        normalized = normalize_phone(value)
    elif identifier_type == "email":
        normalized = normalize_email(value)
    elif identifier_type == "social":
        normalized = normalize_social(value)
    elif identifier_type == "url":
        normalized = normalize_url(value)
    else:
        normalized = normalize_text(value)
    return identifier_type, normalized


def hash_identifier(value: str) -> str:
    _, normalized = normalize_identifier(value)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
