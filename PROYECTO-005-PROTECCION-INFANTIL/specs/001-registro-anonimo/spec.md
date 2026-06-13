# SPEC-001 — Registro Anónimo de Reportes (Módulo 001)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio de 2026  
**Versión:** 2.0 (Actualizado con PWA + Evidencia Multimedia)  
**Autor:** ZEUS / ODIN  
**Estado:** ✅ Completado

---

## 1. RESUMEN

El Módulo 001 permite a cualquier persona, desde cualquier navegador, reportar un contacto inapropiado o intento de abuso hacia un menor, sin exponer su identidad. El reporte incluye: identificador del contacto (teléfono, email, red social), descripción narrativa, y evidencia multimedia opcional (fotos, videos, capturas, audios).

---

## 2. FLUJO DE USUARIO (PWA)

```
[Usuario abre PWA en navegador]
           │
           ▼
[Formulario de reporte — 3 campos máximo]
           │
           ├── Campo 1: Identificador (teléfono, email, @usuario, URL)
           ├── Campo 2: Descripción del incidente (texto libre)
           └── Campo 3: Evidencia multimedia (opcional)
                   ├── 📷 Foto
                   ├── 🎥 Video
                   ├── 🎙️ Audio
                   └── 📄 Captura de pantalla
           │
           ▼
[Review antes de enviar]
           │
           ▼
[POST /api/reportes — Encriptación en backend]
           │
           ▼
[Página de confirmación con hash único]
           │
           └── "Guarda este código: ABC123-XYZ789"
           └── "No podremos contactarte. Este es tu único recibo."
```

---

## 3. ENDPOINTS

### `POST /api/reportes`

**Headers:**
```
Content-Type: application/json
X-No-Track: 1
```

**Body:**
```json
{
  "reported_identifier": "+573001234567",
  "description": "Este número contactó a mi hija de 12 años por WhatsApp pidiendo fotos. Se hace pasar por compañero de colegio.",
  "evidence_type": "image",
  "evidence_content": "base64_encoded_encrypted_image...",
  "evidence_media_url": "https://cdn.semaforo.com/enc/abc123",
  "consent_location": true
}
```

**Response 201:**
```json
{
  "report_hash": "SHA-256-DE-CONFIRMACION-64CHAR",
  "message": "Reporte recibido. Guarde este código como único recibo.",
  "warning": "No podemos contactarlo. No guardamos ningún dato de identificación."
}
```

**Response 429 (Rate limit):**
```json
{
  "error": "Demasiados reportes desde esta conexión. Espere 1 hora.",
  "retry_after": 3600
}
```

---

## 4. ENCRIPTACIÓN (AES-256-GCM)

Cada campo sensible se encripta con:
- **Algoritmo:** AES-256-GCM
- **DEK (Data Encryption Key):** Generado por campo con `os.urandom(32)`
- **KEK (Key Encryption Key):** Almacenado en variable de entorno, nunca en disco
- **Nonce:** 12 bytes aleatorios por operación

**Campos encriptados:**
- `reported_identifier`
- `description`
- `evidence_content` (base64 del archivo encriptado)
- `evidence_media_url` (URL contiene token encriptado)

**Campos NO encriptados (metadata operativa):**
- `id` (UUID, PK)
- `report_hash` (SHA-256 del reporte, para confirmación)
- `evidence_type` (tipo, no contenido)
- `city` / `country` (solo si `consent_location=true`)
- `reported_at` / `updated_at`

---

## 5. EVIDENCIA MULTIMEDIA

| Tipo | Extensiones | Tamaño máximo | Procesamiento |
|------|-------------|---------------|---------------|
| Imagen | .jpg, .png, .webp | 5 MB | Thumbnail 200x200 encriptado, original encriptado |
| Video | .mp4, .mov | 50 MB | Stream HLS encriptado, metadata stripped |
| Audio | .mp3, .m4a, .ogg | 10 MB | Transcripción automática (texto encriptado) |
| Captura | .png, .jpg | 5 MB | OCR para extraer texto, original encriptado |

**Procesamiento de seguridad:**
1. Strip EXIF GPS y metadata del archivo
2. Generar thumbnail/vista previa
3. Encriptar con AES-256-GCM
4. Almacenar en filesystem con nombre aleatorio (no el original)
5. URL accesible solo con token de admin + desencriptación bajo demanda

---

## 6. CATEGORÍAS DE REPORTE

El usuario selecciona una categoría al reportar. Esto alimenta el modelo de IA del Módulo 003:

| Código | Categoría | Descripción | Peso IA |
|--------|-----------|-------------|---------|
| CAT-01 | Contacto inapropiado | Mensaje, llamada, o contacto no solicitado | 0.3 |
| CAT-02 | Solicitud de material sexual | Pide fotos, videos, o descripción de cuerpo | 0.8 |
| CAT-03 | Grooming / Engaño | Se hace pasar por menor para ganar confianza | 0.9 |
| CAT-04 | Cita en persona | Propone encuentro físico con menor | 0.95 |
| CAT-05 | Extorsión | Amenaza con difundir material para obtener más | 0.85 |
| CAT-06 | Desconocido | No aplica o no está claro | 0.1 |

---

## 7. ANONIMATO ABSOLUTO

| Dato | ¿Almacenado? | Nota |
|------|-------------|------|
| IP | ❌ No | Nginx log desactivado para este endpoint |
| User-Agent | ❌ No | No se lee ni almacena |
| Cookies | ❌ No | Zero cookies |
| localStorage | ❌ No | No se usa |
| Session / JWT | ❌ No | Sin autenticación |
| Fingerprint | ❌ No | Sin Canvas, WebGL, Fonts |
| Timestamp exacto | ⚠️ Solo fecha | Hora truncada a franja de 6 horas |
| Ciudad/País | ⚠️ Solo si consiente | Geocodificación aproximada, no exacta |

---

## 8. RATE LIMITING

| Recurso | Límite | Ventana |
|---------|--------|---------|
| POST /api/reportes | 5 | 1 hora por IP |
| GET /api/validate/{id} | 10 | 1 hora por IP |
| GET /api/health | 100 | 1 hora por IP |
| Upload evidencia | 3 | 1 hora por IP |

**Implementación:** Redis `INCR` con `EXPIRE 3600`. IP se hashea con SHA-256 antes de almacenar en Redis.

---

## 9. CRITERIOS DE ACEPTACIÓN (DoD)

- [x] Formulario funciona en móvil (viewport 320px+)
- [x] POST /api/reportes retorna hash único de 64 caracteres
- [x] Encriptación AES-256-GCM — validado con test de cifrado/descifrado
- [x] Rate limiting funciona — 6to reporte retorna 429
- [x] Ningún header de tracking en response
- [x] Evidencia multimedia se encripta y almacena correctamente
- [x] Thumbnail se genera para imágenes
- [x] EXIF se elimina antes de encriptar
- [x] Cobertura de tests ≥ 80%
- [x] PWA instala desde navegador (manifest + service worker)

---

> *SPEC generado por ODIN — Innovadataco*  
> *Versión 2.0 — Actualizado con PWA, evidencia multimedia, categorías*
