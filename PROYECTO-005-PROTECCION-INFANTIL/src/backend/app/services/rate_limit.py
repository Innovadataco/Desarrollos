import hashlib
import logging
import time
from collections import defaultdict
from threading import Lock

from fastapi import HTTPException, Request
from limits import RateLimitItemPerHour
from limits.storage import MemoryStorage, RedisStorage
from limits.strategies import MovingWindowRateLimiter

from app.config import settings

logger = logging.getLogger(__name__)

MAX_MEMORY_KEYS = 1000

DEFAULT_LIMITS = {
    "report": 5,
    "validate": 10,
    "health": 100,
    "login": 5,
    "decrypt": 10,
    "gateway": 100,
    "admin": 1000,
}


def _build_limiter():
    if settings.redis_url:
        try:
            storage = RedisStorage(settings.redis_url)
            logger.info("Rate limiting usando Redis: %s", settings.redis_url)
            return MovingWindowRateLimiter(storage)
        except Exception as exc:
            logger.warning(
                "No se pudo conectar a Redis para rate limiting: %s. Fallback a memoria.",
                exc,
            )

    if settings.environment.lower() == "production":
        logger.warning(
            "Rate limiting en memoria activo en producción. "
            "No escala entre workers/replicas. Configure REDIS_URL."
        )
    return MovingWindowRateLimiter(MemoryStorage())


_limiter = _build_limiter()


class InMemoryRateLimiter:
    """
    Rate limiter en memoria de respaldo. No persiste IPs: las entradas expiran
    cuando pasa la ventana de tiempo. Capado a MAX_MEMORY_KEYS para evitar
    crecimiento ilimitado.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._store: dict[str, tuple[int, float]] = defaultdict(
            lambda: (0, time.time())
        )
        self._lock = Lock()

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        with self._lock:
            self._cleanup_if_needed(now)
            count, window_start = self._store[key]
            if now - window_start >= self.window_seconds:
                self._store[key] = (1, now)
                return True
            if count >= self.max_requests:
                return False
            self._store[key] = (count + 1, window_start)
            return True

    def reset(self):
        with self._lock:
            self._store.clear()

    def _cleanup_if_needed(self, now: float):
        if len(self._store) < MAX_MEMORY_KEYS:
            return
        cutoff = now - self.window_seconds
        expired = [k for k, (_, start) in self._store.items() if start < cutoff]
        for k in expired:
            del self._store[k]


# Respaldos para tests y desarrollo sin Redis
_fallback_limiters = {
    name: InMemoryRateLimiter(max_requests=limit, window_seconds=3600)
    for name, limit in DEFAULT_LIMITS.items()
}
_fallback_limiters["login"] = InMemoryRateLimiter(max_requests=5, window_seconds=900)


def _using_memory_storage() -> bool:
    return isinstance(getattr(_limiter, "storage", None), MemoryStorage)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _make_key(scope: str, identifier: str) -> str:
    # Normalizamos y hasheamos el identificador (IP) para no almacenar PII.
    normalized = identifier.strip().lower().encode("utf-8")
    hashed = hashlib.sha256(normalized).hexdigest()
    return f"{scope}:{hashed}"


def check_rate_limit(
    request: Request, scope: str = "report", identifier: str | None = None
):
    key = identifier or get_client_ip(request)
    limit = DEFAULT_LIMITS.get(scope, 5)

    if _using_memory_storage():
        limiter = _fallback_limiters.get(scope, _fallback_limiters["report"])
        if not limiter.is_allowed(key):
            raise HTTPException(
                status_code=429,
                detail="Has alcanzado el límite de solicitudes. Intenta más tarde.",
            )
        return

    item = RateLimitItemPerHour(limit)
    if not _limiter.hit(item, _make_key(scope, key)):
        raise HTTPException(
            status_code=429,
            detail="Has alcanzado el límite de solicitudes. Intenta más tarde.",
        )


def reset_fallback_limiters():
    for limiter in _fallback_limiters.values():
        limiter.reset()
