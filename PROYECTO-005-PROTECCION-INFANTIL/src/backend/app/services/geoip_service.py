"""Servicio de geocodificación aproximada para clustering.

La IP del reportante nunca se almacena: se hashea y descarta inmediatamente.
Solo se conserva ciudad/país aproximado cuando el usuario da consentimiento.
"""

import hashlib
import logging
import os
from pathlib import Path

from fastapi import Request

from app.config import settings

logger = logging.getLogger(__name__)


def _hash_ip(ip: str) -> str:
    """SHA-256 de la IP; el valor original se descarta."""
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()


def _mmdb_path() -> Path:
    """Ruta a la base GeoLite2-City local."""
    if settings.geolite2_path:
        return Path(settings.geolite2_path)
    return Path("data") / "GeoLite2-City.mmdb"


def _location_from_geolite2(ip: str) -> tuple[str | None, str | None]:
    """Intenta resolver ciudad/país con MaxMind GeoLite2 local."""
    mmdb = _mmdb_path()
    if not mmdb.exists():
        return None, None

    try:
        import geoip2.database

        with geoip2.database.Reader(str(mmdb)) as reader:
            response = reader.city(ip)
            city = response.city.name
            country = response.country.name
            return city, country
    except Exception as exc:  # pragma: no cover - GeoLite2 puede no estar disponible
        logger.debug("GeoLite2 no pudo resolver %s: %s", _hash_ip(ip), exc)
        return None, None


def _location_from_headers(request: Request) -> tuple[str | None, str | None]:
    """Fallback a cabeceras enviadas por el cliente/proxy."""
    city = request.headers.get("x-client-city")
    country = request.headers.get("x-client-country")
    return city, country


def get_location_from_ip(
    ip: str, request: Request, consent: bool = True
) -> tuple[str | None, str | None]:
    """Resuelve ciudad/país aproximado desde una IP.

    - Si `consent` es False, retorna (None, None).
    - Hashea la IP inmediatamente; la IP original nunca se devuelve ni almacena.
    - Si existe GeoLite2-City.mmdb local, lo usa.
    - Si no, usa las cabeceras X-Client-City / X-Client-Country.
    - Coordenadas exactas, código postal, etc. nunca se consultan ni guardan.
    """
    if not consent:
        return None, None

    # Hashear y descartar la IP original antes de cualquier otra operación.
    _hash_ip(ip)

    city, country = _location_from_geolite2(ip)
    if city or country:
        return city, country

    return _location_from_headers(request)
