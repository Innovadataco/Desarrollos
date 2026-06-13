from app.services.identifier import (
    detect_identifier_type,
    hash_identifier,
    normalize_identifier,
)


def test_normalize_phone():
    t, normalized = normalize_identifier("+57 300 123 4567")
    assert t == "phone"
    assert "+573001234567" in normalized


def test_normalize_phone_without_plus():
    t, normalized = normalize_identifier("57 300 123 4567")
    assert t == "phone"
    assert normalized == "573001234567"


def test_normalize_email():
    t, normalized = normalize_identifier("Test@Example.COM")
    assert t == "email"
    assert normalized == "test@example.com"


def test_normalize_social():
    t, normalized = normalize_identifier("@Usuario_Malo")
    assert t == "social"
    assert normalized == "usuario_malo"


def test_normalize_url():
    t, normalized = normalize_identifier("HTTPS://Example.com/path")
    assert t == "url"
    assert "example.com/path" in normalized


def test_normalize_url_strips_query_params():
    t, normalized = normalize_identifier("https://Example.com/path?ref=123&x=1")
    assert t == "url"
    assert "?" not in normalized
    assert normalized == "example.com/path"


def test_normalize_email_variants():
    variants = [
        "Test@Example.COM",
        "  Test@Example.COM  ",
        "test@example.com",
    ]
    hashes = {hash_identifier(v) for v in variants}
    assert len(hashes) == 1, "Variantes de email deben normalizar al mismo hash"


def test_detect_identifier_type():
    assert detect_identifier_type("+573001234567") == "phone"
    assert detect_identifier_type("a@b.com") == "email"
    assert detect_identifier_type("@user") == "social"
    assert detect_identifier_type("https://x.com") == "url"
    assert detect_identifier_type("solo texto") == "text"


def test_hash_consistency():
    h1 = hash_identifier("test@example.com")
    h2 = hash_identifier("test@example.com")
    assert h1 == h2
    assert len(h1) == 64


def test_hash_sha256_and_uniqueness():
    import hashlib

    value = "+573001234567"
    expected = hashlib.sha256("+573001234567".encode("utf-8")).hexdigest()
    assert hash_identifier(value) == expected

    h1 = hash_identifier("usuario1")
    h2 = hash_identifier("usuario2")
    assert h1 != h2


def test_hash_is_case_insensitive_for_social():
    h1 = hash_identifier("@UsuarioMalo")
    h2 = hash_identifier("@usuariomalo")
    assert h1 == h2
