import logging
import time
from collections import defaultdict
from threading import Lock

from fastapi import HTTPException, Request
from limits import RateLimitItemPerMinute
from limits.storage import MemoryStorage, RedisStorage
from limits.strategies import MovingWindowRateLimiter

from app.config import settings

logger = logging.getLogger(__name__)

MAX_MEMORY_KEYS = 1000


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
_rate_limit_item = RateLimitItemPerMinute(5)


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
_fallback_rate_limiter = InMemoryRateLimiter()


def _using_memory_storage() -> bool:
    return isinstance(getattr(_limiter, "storage", None), MemoryStorage)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request):
    ip = get_client_ip(request)

    if _using_memory_storage():
        if not _fallback_rate_limiter.is_allowed(ip):
            raise HTTPException(
                status_code=429,
                detail="Has alcanzado el límite de reportes. Intenta más tarde.",
            )
        return

    if not _limiter.hit(_rate_limit_item, ip):
        raise HTTPException(
            status_code=429,
            detail="Has alcanzado el límite de reportes. Intenta más tarde.",
        )
