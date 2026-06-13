import hashlib
import secrets
import struct

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AAD = b"proteccion-infantil-v1"


def derive_kek(key_hex: str) -> bytes:
    """Decodifica la clave maestra desde hex. Debe ser exactamente 32 bytes."""
    key = bytes.fromhex(key_hex)
    if len(key) != 32:
        raise ValueError(
            "REPORT_ENCRYPTION_KEY debe ser exactamente 32 bytes (64 caracteres hex)"
        )
    return key


def _encrypt(plaintext: str, key: bytes) -> bytes:
    """Encripta texto con AES-256-GCM. Retorna nonce(12) + tag(16) + ciphertext."""
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), AAD)
    return nonce + ciphertext


def _decrypt(blob: bytes, key: bytes) -> str:
    """Desencripta un blob AES-256-GCM."""
    if len(blob) < 28:
        raise ValueError("Blob encriptado inválido")
    nonce = blob[:12]
    ciphertext = blob[12:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, AAD)
    return plaintext.decode("utf-8")


def encrypt_field(plaintext: str, kek: bytes) -> bytes:
    """
    Encripta un campo usando una DEK aleatoria.
    Formato: [len_encrypted_dek: 2 bytes][encrypted_dek][nonce||tag||ciphertext]
    """
    dek = AESGCM.generate_key(bit_length=256)
    encrypted_dek = _encrypt(dek.hex(), kek)
    encrypted_value = _encrypt(plaintext, dek)
    return struct.pack(">H", len(encrypted_dek)) + encrypted_dek + encrypted_value


def decrypt_field(blob: bytes, kek: bytes) -> str:
    """Desencripta un campo encriptado con encrypt_field."""
    if len(blob) < 2:
        raise ValueError("Blob inválido")
    encrypted_dek_len = struct.unpack(">H", blob[:2])[0]
    offset = 2 + encrypted_dek_len
    encrypted_dek = blob[2:offset]
    encrypted_value = blob[offset:]
    dek_hex = _decrypt(encrypted_dek, kek)
    dek = bytes.fromhex(dek_hex)
    return _decrypt(encrypted_value, dek)


def generate_report_hash(identifier: str, timestamp_iso: str) -> str:
    """
    Genera un hash único no vinculable al reportante.
    Usa un nonce aleatorio para evitar que el hash sea determinista fuera del sistema.
    """
    nonce = secrets.token_hex(16)
    payload = f"{nonce}:{timestamp_iso}:{identifier.strip().lower()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_identifier(identifier: str) -> str:
    """SHA-256 canonizado para indexar reportes sin revelar el identificador."""
    return hashlib.sha256(identifier.strip().lower().encode("utf-8")).hexdigest()
