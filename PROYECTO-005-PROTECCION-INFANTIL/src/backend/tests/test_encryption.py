import pytest
from cryptography.exceptions import InvalidTag

from app.services.encryption import decrypt_field, derive_kek, encrypt_field


@pytest.fixture
def kek():
    return derive_kek(
        "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    )


def test_encrypt_decrypt_roundtrip(kek):
    plaintext = "+573001234567"
    encrypted = encrypt_field(plaintext, kek)
    decrypted = decrypt_field(encrypted, kek)
    assert decrypted == plaintext


def test_different_ciphertexts_for_same_plaintext(kek):
    plaintext = "mensaje repetido"
    encrypted1 = encrypt_field(plaintext, kek)
    encrypted2 = encrypt_field(plaintext, kek)
    assert encrypted1 != encrypted2
    assert decrypt_field(encrypted1, kek) == plaintext
    assert decrypt_field(encrypted2, kek) == plaintext


def test_tampering_detection(kek):
    encrypted = bytearray(encrypt_field("secreto", kek))
    encrypted[-1] ^= 0xFF  # modifica último byte
    with pytest.raises(InvalidTag):
        decrypt_field(bytes(encrypted), kek)


def test_invalid_kek_length():
    with pytest.raises(ValueError):
        derive_kek("corta")
