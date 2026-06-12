import time
from collections import defaultdict
from threading import Lock
from fastapi import Request, HTTPException


class InMemoryRateLimiter:
    """
    Rate limiter en memoria. No persiste IPs: las entradas expiran
    cuando pasa la ventana de tiempo.
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


rate_limiter = InMemoryRateLimiter()


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request):
    ip = get_client_ip(request)
    if not rate_limiter.is_allowed(ip):
        raise HTTPException(
            status_code=429,
            detail="Has alcanzado el límite de reportes. Intenta más tarde.",
        )
