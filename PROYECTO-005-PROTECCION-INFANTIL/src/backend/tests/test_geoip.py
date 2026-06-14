import pytest
from starlette.requests import Request

from app.services.geoip_service import _hash_ip, get_location_from_ip


def _make_request(headers=None):
    headers = headers or []
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "headers": headers,
        }
    )


def test_get_location_without_consent():
    request = _make_request()
    assert get_location_from_ip("8.8.8.8", request, consent=False) == (None, None)


def test_get_location_fallback_headers():
    request = _make_request(
        [
            (b"x-client-city", b"Medellin"),
            (b"x-client-country", b"CO"),
        ]
    )
    city, country = get_location_from_ip("8.8.8.8", request, consent=True)
    assert city == "Medellin"
    assert country == "CO"


def test_get_location_geolite2_when_available(monkeypatch, tmp_path):
    """Si existe GeoLite2-City.mmdb, se usa antes que las cabeceras."""

    class FakeCity:
        name = "Bogotá"

    class FakeCountry:
        name = "Colombia"

    class FakeResponse:
        city = FakeCity()
        country = FakeCountry()

    class FakeReader:
        def __init__(self, path):
            self.path = path

        def city(self, ip):
            return FakeResponse()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(
        "app.services.geoip_service._mmdb_path", lambda: tmp_path / "GeoLite2-City.mmdb"
    )
    (tmp_path / "GeoLite2-City.mmdb").write_text("fake-mmdb")

    # Mockear geoip2.database.Reader solo para este test.
    import geoip2.database

    monkeypatch.setattr(geoip2.database, "Reader", FakeReader)

    request = _make_request(
        [
            (b"x-client-city", b"Medellin"),
            (b"x-client-country", b"CO"),
        ]
    )
    city, country = get_location_from_ip("1.1.1.1", request, consent=True)
    assert city == "Bogotá"
    assert country == "Colombia"


def test_ip_is_hashed_not_stored():
    ip = "192.168.1.100"
    hashed = _hash_ip(ip)
    assert hashed != ip
    assert len(hashed) == 64
