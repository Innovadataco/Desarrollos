# BITÁCORA-001 — Correcciones ODIN-001 al Módulo 001

**Proyecto:** Semáforo de Confianza (005)  
**Rama activa:** `feature/v2-fullstack`  
**Auditoría consultada:** `setup/estructura-2026` (`docs/auditoria/`)  
**Fecha de inicio:** 13 de junio de 2026  
**Responsable:** ODIN

---

## Objetivo

Aplicar correcciones autónomas a las deudas técnicas críticas detectadas por ZEUS en el Módulo 001, **sin modificar los artefactos de auditoría**.

---

## 1. Rate limiting

### Hallazgo
El limitador usaba `RateLimitItemPerMinute` y la IP en claro como clave.

### Acción
- Se cambia a `RateLimitItemPerHour(5)` para el scope `report`.
- Se hashea la IP con SHA-256 antes de construir la clave (`scope:hash`).
- El fallback en memoria mantiene ventana de 3600 s.

### Archivos
- `src/backend/app/services/rate_limit.py`

---

## 2. Encriptación AES-256-GCM con AAD

### Hallazgo
Faltaba datos adicionales autenticados (AAD) en el cifrado.

### Acción
- Se añade `AAD = b"proteccion-infantil-v1"` a `_encrypt` / `_decrypt`.
- Se agregan `encrypt_file` / `decrypt_file` para evidencia multimedia.

### Archivos
- `src/backend/app/services/encryption.py`

---

## 3. Modelo de datos y anonimato temporal

### Hallazgo
Faltaban campos del SPEC y el timestamp guardaba precisión completa.

### Acción
- Se confirman `category`, `consent_location`, `city`, `country` en `Report`.
- Se añade `reported_at_bucket` truncado a 6 horas.
- Se crea utilidad `app/utils/time.py`.

### Archivos
- `src/backend/app/models.py`
- `src/backend/app/routers/reportes.py`
- `src/backend/app/utils/time.py`

---

## 4. Honeypot anti-spam

### Hallazgo
No existía mecanismo anti-bot.

### Acción
- Frontend: campo invisible `name="website"`.
- Backend: rechazo silencioso si `honeypot` no está vacío, con registro en `AuditLog`.

### Archivos
- `src/frontend/src/components/ReportForm.jsx`
- `src/backend/app/schemas.py`
- `src/backend/app/routers/reportes.py`

---

## 5. Review step y copiar hash

### Hallazgo
No había paso de revisión ni botón para copiar el hash de confirmación.

### Acción
- El wizard pasa de 3 a 4 pasos; el paso 4 muestra resumen y checkbox de confirmación.
- En pantalla de éxito se añade botón "Copiar código" con `navigator.clipboard`.

### Archivos
- `src/frontend/src/components/ReportForm.jsx`

---

## 6. Evidencia multimedia segura

### Hallazgo
Los adjuntos se almacenaban sin strip EXIF, sin thumbnail y sin encriptar.

### Acción
- Se implementa strip EXIF best-effort con Pillow.
- Se genera thumbnail encriptado para imágenes.
- Se encripta el archivo con AES-256-GCM y DEK por archivo.
- Se añaden columnas `thumbnail_path` e `is_encrypted` al modelo `Evidence`.
- `read_evidence_file` desencripta bajo demanda.

### Archivos
- `src/backend/app/services/evidence_service.py`
- `src/backend/app/models.py`

---

## 7. Infraestructura Docker

### Hallazgo
`docker-compose.yml` solo levantaba backend + frontend.

### Acción
- Se añaden servicios `postgres:16-alpine`, `redis:7-alpine` y `nginx:alpine`.
- Se configura `access_log off` para `/api/reportes`.
- Se documenta TLS 1.3 en `nginx/nginx.conf` (requiere certificados).
- Se crean Dockerfiles multi-stage para backend (`base` → `development` / `production`) y frontend (`builder` + `nginx`).
- Se añade `.env.example` con variables para PostgreSQL y Redis.

### Archivos
- `docker-compose.yml`
- `src/backend/Dockerfile`
- `src/frontend/Dockerfile`
- `nginx/nginx.conf`
- `src/frontend/nginx.conf`
- `.env.example`

---

## 8. Estados "COMPLETADO" corregidos

### Hallazgo
El Módulo 001 fue declarado completado sin validación.

### Acción
- Se cambian los estados a `🚧 EN CORRECCIÓN / NO VALIDADO` en:
  - `specs/001-registro-anonimo/spec.md`
  - `specs/001-registro-anonimo/plan.md`
  - `specs/001-registro-anonimo/tasks.md`
  - `README.md`
- Se añaden notas explicando que no se marcarán ítems hasta el Acta de Validación de ZEUS.

---

## 9. Documentación de metodología

### Acción
- Se crea `docs/LECCIONES-001.md`.
- Se crea `docs/BITACORA-001.md` (este documento).
- Se crea `.github/pull_request_template.md` con DoD checklist.

---

## Pendientes reconocidos

- [ ] Migrar frontend a TypeScript (baja prioridad).
- [ ] Ejecutar validación E2E de Playwright tras los cambios del wizard.
- [ ] Revisar CORS y allowed hosts para producción.
- [ ] Implementar certificados TLS 1.3 reales en el despliegue.
- [ ] Obtener Acta de Validación firmada por ZEUS.

---

> *Bitácora generada por ODIN. No modificar `docs/auditoria/`.*
