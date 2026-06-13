import time

from app.services import cache_service


def test_cache_memory_set_get():
    cache_service.clear()
    cache_service.set("hash1", {"semaforo": "verde"}, ttl_seconds=2)
    assert cache_service.get("hash1") == {"semaforo": "verde"}


def test_cache_memory_expires():
    cache_service.clear()
    cache_service.set("hash1", {"semaforo": "verde"}, ttl_seconds=1)
    time.sleep(1.1)
    assert cache_service.get("hash1") is None


def test_cache_clear():
    cache_service.set("hash1", {"semaforo": "verde"})
    cache_service.clear()
    assert cache_service.get("hash1") is None
