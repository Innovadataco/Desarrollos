"""Cache simple para resultados de consulta, con Redis o fallback en memoria."""

import json
from datetime import datetime, timezone
from typing import Any

from app.config import settings

_redis_client = None
_memory_cache: dict[str, tuple[str, float]] = {}


def _get_redis():
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not settings.redis_url:
        return None
    try:
        import redis

        _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        _redis_client.ping()
        return _redis_client
    except Exception:
        return None


def _key(identifier_hash: str) -> str:
    return f"consulta:{identifier_hash}"


def get(identifier_hash: str) -> dict[str, Any] | None:
    key = _key(identifier_hash)
    client = _get_redis()
    if client:
        value = client.get(key)
        if value:
            return json.loads(value)
        return None

    # Fallback en memoria con TTL de 5 minutos.
    entry = _memory_cache.get(key)
    if not entry:
        return None
    value, expires = entry
    if datetime.now(timezone.utc).timestamp() > expires:
        del _memory_cache[key]
        return None
    return json.loads(value)


def set(identifier_hash: str, data: dict[str, Any], ttl_seconds: int = 300) -> None:
    key = _key(identifier_hash)
    payload = json.dumps(data)
    client = _get_redis()
    if client:
        client.setex(key, ttl_seconds, payload)
        return
    expires = datetime.now(timezone.utc).timestamp() + ttl_seconds
    _memory_cache[key] = (payload, expires)


def get_key(key: str) -> Any | None:
    """Obtiene cualquier valor cacheado por clave exacta."""
    client = _get_redis()
    if client:
        value = client.get(key)
        if value:
            return json.loads(value)
        return None

    entry = _memory_cache.get(key)
    if not entry:
        return None
    value, expires = entry
    if datetime.now(timezone.utc).timestamp() > expires:
        del _memory_cache[key]
        return None
    return json.loads(value)


def set_key(key: str, data: Any, ttl_seconds: int = 300) -> None:
    """Guarda cualquier valor JSON-serializable bajo una clave exacta."""
    payload = json.dumps(data)
    client = _get_redis()
    if client:
        client.setex(key, ttl_seconds, payload)
        return
    expires = datetime.now(timezone.utc).timestamp() + ttl_seconds
    _memory_cache[key] = (payload, expires)


def delete_key(key: str) -> None:
    """Elimina una clave del cache."""
    client = _get_redis()
    if client:
        client.delete(key)
    _memory_cache.pop(key, None)


def clear() -> None:
    global _memory_cache
    client = _get_redis()
    if client:
        for key in client.scan_iter(match="consulta:*"):
            client.delete(key)
    _memory_cache = {}
