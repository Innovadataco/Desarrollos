# ADR-001 — Encriptación AES-256-GCM

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 2.0 (Actualizado con evidencia multimedia)  
**Autor:** ZEUS / ODIN  
**Estado:** ✅ Aprobado

---

## Contexto

La plataforma maneja datos extremadamente sensibles: reportes de contacto inapropiado con menores, descripciones de incidentes, y ahora evidencia multimedia (fotos, videos, audios, capturas de pantalla). La protección de estos datos es crítica para la seguridad de los reportantes y la integridad de la plataforma.

## Decisión

**Usar AES-256-GCM con DEK (Data Encryption Key) por campo para todos los datos sensibles, incluyendo evidencia multimedia.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| AES-256-CBC | Más simple, compatible | No autenticación, vulnerable a padding oracle | ❌ Rechazado |
| AES-256-GCM | Autenticación integrada, eficiente | Más complejo de implementar | ✅ Elegido |
| ChaCha20-Poly1305 | Muy seguro, rápido en móvil | Menos soporte en Python/PostgreSQL | ❌ Rechazado |
| Encriptación a nivel de BD (TDE) | Transparente, fácil | No protege contra acceso a BD por admin | ❌ Rechazado |
| HSM (Hardware Security Module) | Máxima seguridad | Costo, complejidad, dependencia física | ⚠️ Futuro |

## Consecuencias

### Positivas
- Autenticación integrada: cualquier modificación del cifrado se detecta (GCM tag)
- DEK por campo: compromiso de una clave no afecta otros campos
- KEK en variable de entorno: nunca en código ni repo
- Rápido y eficiente: Python cryptography nativo

### Negativas
- No se puede indexar ni buscar en campos encriptados (resuelto con identifier_hash)
- Rotación de claves requiere re-encriptación de todos los datos
- KEK en env var: si el servidor es comprometido, la KEK está en memoria (aceptable para MVP)

## Implementación

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, base64

# KEK (Key Encryption Key) — variable de entorno, nunca en código
KEK = os.environb[b"PROTECCION_KEK"]  # 32 bytes de os.urandom(32)

def generate_dek() -> bytes:
    """Genera un DEK único de 32 bytes."""
    return AESGCM.generate_key(bit_length=256)

def encrypt_field(plaintext: str) -> str:
    """Encripta un campo con DEK único, luego encripta el DEK con KEK."""
    dek = generate_dek()
    nonce = os.urandom(12)
    aad = b"proteccion-infantil-v1"  # Associated data
    
    aesgcm = AESGCM(dek)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad)
    
    # Encriptar DEK con KEK
    aesgcm_kek = AESGCM(KEK)
    dek_nonce = os.urandom(12)
    encrypted_dek = aesgcm_kek.encrypt(dek_nonce, dek, aad)
    
    # Formato: base64(encrypted_dek) + ":" + base64(dek_nonce) + ":" + base64(nonce) + ":" + base64(ciphertext)
    return f"{base64.b64encode(encrypted_dek).decode()}:{base64.b64encode(dek_nonce).decode()}:{base64.b64encode(nonce).decode()}:{base64.b64encode(ciphertext).decode()}"

def decrypt_field(encrypted: str) -> str:
    """Desencripta un campo."""
    enc_dek, dek_nonce, nonce, ciphertext = map(base64.b64decode, encrypted.split(":"))
    
    aad = b"proteccion-infantil-v1"
    aesgcm_kek = AESGCM(KEK)
    dek = aesgcm_kek.decrypt(dek_nonce, enc_dek, aad)
    
    aesgcm = AESGCM(dek)
    plaintext = aesgcm.decrypt(nonce, ciphertext, aad)
    
    return plaintext.decode("utf-8")
```

### Evidencia Multimedia

| Tipo | Proceso | Encriptación |
|------|---------|--------------|
| Imagen | Strip EXIF → Thumbnail → Encriptar original + thumbnail | AES-256-GCM |
| Video | Strip metadata → HLS segments → Encriptar cada segmento | AES-256-GCM |
| Audio | Strip metadata → Transcripción → Encriptar audio + texto | AES-256-GCM |
| Captura | Strip metadata → OCR → Encriptar imagen + texto | AES-256-GCM |

**Almacenamiento:** Filesystem con nombre aleatorio (UUID). No el nombre original del archivo. No directorio estructurado por fecha (evita correlación temporal).

**URL de evidencia:** Token JWT temporal (5 min) + endpoint autenticado (admin). Nunca URL directa a archivo.

## Campos Encriptados

| Entidad | Campo | Tipo | Encriptado |
|---------|-------|------|------------|
| Report | `reported_identifier` | String | ✅ Sí (DEK) |
| Report | `description` | Text | ✅ Sí (DEK) |
| Report | `evidence_content` | LargeBinary | ✅ Sí (DEK) |
| Report | `evidence_media_url` | String | ✅ Sí (DEK) |
| Analysis | `explanation` | JSON | ✅ Sí (DEK) |
| Profile | `identifier_hash` | String | ❌ No (hash, irreversible) |

## Notas

- KEK generada con `openssl rand -base64 32`
- KEK rotada manualmente cada 6 meses (MVP), automáticamente en futuro (HSM)
- Re-encriptación: script batch que descifra con KEK vieja, cifra con KEK nueva
- Backup de KEK: encriptada con GPG y almacenada offline (cofre físico de Diana)

---

> *ADR generado por ODIN — Innovadataco*  
> *Versión 2.0 — Actualizado con evidencia multimedia*
