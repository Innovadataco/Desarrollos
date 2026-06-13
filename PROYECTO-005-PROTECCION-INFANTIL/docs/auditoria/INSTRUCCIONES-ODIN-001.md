# INSTRUCCIONES PARA ODIN — Corrección del Módulo 001
**Proyecto:** PROYECTO-005 — Protección Infantil (Semáforo de Confianza)  
**Módulo:** 001 — Registro Anónimo  
**Fecha:** 14 de junio de 2026  
**Autor:** ZEUS (CEO PMO)  
**Destinatario:** ODIN (Agente de Desarrollo)  
**Estatus:** OBLIGATORIO — Seguir en orden, sin saltar pasos

---

## 🚨 ANTES DE EMPEZAR — LEE ESTO

El Módulo 001 fue declarado "COMPLETADO" pero ZEUS encontró que solo está al **65%** real.

**Lo que NO debes hacer:**
- ❌ No toques el Módulo 002 hasta que ZEUS apruebe el 001
- ❌ No declares "completado" sin pasar DoD checklist
- ❌ No mergees a `main` sin PR y aprobación

**Lo que SÍ debes hacer:**
- ✅ Seguir estas instrucciones en ORDEN
- ✅ Marcar cada task con DoD checklist (ver abajo)
- ✅ Crear PR cuando termines una fase
- ✅ Solicitar validación de ZEUS antes de declarar "listo"

---

## 📋 DEFINITION OF DONE (DoD) — APLICAR A CADA TASK

```markdown
### DoD Checklist (copiar y pegar en cada task)
- [ ] Código implementado y funcional
- [ ] Tests unitarios pasan (`pytest -v` / `npm test`)
- [ ] Tests de integración pasan
- [ ] Cobertura ≥ 80% (`pytest --cov` / `vitest --coverage`)
- [ ] Linter pasa sin errores (`ruff check` / `eslint`)
- [ ] Commit sigue Conventional Commits: `fix(PROYECTO-005): ...`
- [ ] Documentación técnica actualizada (si aplica)
- [ ] No hay secrets hardcodeados
- [ ] Security checklist pasa para esta task
- [ ] Review por ZEUS (o auto-review documentada en PR)
```

**Regla:** Si falta UN check, la task está ⬜ **NO completada**.

---

## 🎯 FASE 1: FIX ESTADO DE DOCUMENTACIÓN (Inmediato — 2h)

**Objetivo:** Corregir la información falsa antes de que el CEO tome decisiones erróneas.

### Task F1.1: Corregir estado en specs/001-registro-anonimo/spec.md
```
Cambiar: "Estado: ✅ Completado"
A:      "Estado: ⚠️ 65% Completado — En corrección (ver docs/auditoria/ACTA-CORRECCION-ODIN-001.md)"
```
**DoD:** ✅ Commit con mensaje claro. ZEUS verifica.

### Task F1.2: Corregir estado en specs/001-registro-anonimo/plan.md
```
Cambiar: "Estado: ✅ COMPLETADO"
A:      "Estado: ⚠️ En corrección — 15 acciones pendientes"
```
**DoD:** ✅ Commit con mensaje claro. ZEUS verifica.

### Task F1.3: Corregir estado en specs/001-registro-anonimo/tasks.md
```
Revisar TODAS las tasks marcadas ✅. 
Si NO está en código funcional + testeado → cambiar a ⬜
```
**DoD:** ✅ Solo tasks con DoD completo pueden estar ✅. ZEUS verifica.

### Task F1.4: Corregir estado en README.md
```
Cambiar: "Módulo 001: Registro Anónimo (COMPLETADO)"
A:      "Módulo 001: Registro Anónimo (⚠️ En corrección — 65% real)"
```
**DoD:** ✅ Commit con mensaje claro. ZEUS verifica.

---

## 🎯 FASE 2: FIX BUGS CRÍTICOS DE SEGURIDAD (Semana 1 — Prioridad 🔴)

### Task F2.1: Fix Rate Limiting (AC-002)
**Archivos:** `app/services/rate_limit.py`, `app/routers/reportes.py`
**Cambios:**
1. Cambiar `RateLimitItemPerMinute(5)` → `RateLimitItemPerHour(5)`
2. Hashear IP con SHA-256 antes de usar como clave de rate limit
3. Añadir test: 6to request en 1 hora retorna 429

**DoD:**
- [ ] Código cambiado
- [ ] Test pasa (verifica 6to request = 429)
- [ ] Linter pasa
- [ ] Commit: `fix(PROYECTO-005): corrige rate limit a 5/hora + hash IP`

### Task F2.2: Ampliar Modelo de Datos (AC-003)
**Archivos:** `app/models.py`, `app/schemas.py`, `app/routers/reportes.py`
**Cambios:**
1. Añadir al modelo `Report`: `category` (String, nullable), `consent_location` (Boolean, default=False), `city` (String, nullable), `country` (String, nullable), `evidence_media_url` (String, nullable)
2. Añadir a schemas: `ReportCreate` con campos nuevos, `ReportResponse` con campos nuevos
3. Truncar `reported_at` a franjas de 6 horas (00:00, 06:00, 12:00, 18:00)
4. Crear migración Alembic

**DoD:**
- [ ] Migración funciona (`alembic upgrade head`)
- [ ] Tests de modelo pasan
- [ ] Tests de router pasan
- [ ] Linter pasa
- [ ] Commit: `feat(PROYECTO-005): añade campos faltantes al modelo Report`

### Task F2.3: Implementar Selector de Categorías (AC-003)
**Archivos:** `src/frontend/src/components/ReportForm.jsx`, `app/routers/reportes.py`
**Cambios:**
1. Añadir `<select>` con 6 opciones: CAT-01 (Solicitud de material sexual), CAT-02 (Contacto físico inapropiado), CAT-03 (Grooming / Acicalamiento), CAT-04 (Extorsión), CAT-05 (Contacto repetido), CAT-06 (Otro)
2. Validación en backend: solo aceptar CAT-01 a CAT-06
3. Test: rechazar categoría inválida

**DoD:**
- [ ] Selector visible en frontend
- [ ] Validación en backend
- [ ] Tests E2E pasan (flujo completo con categoría)
- [ ] Linter pasa
- [ ] Commit: `feat(PROYECTO-005): añade selector de categorías 6 opciones`

---

## 🎯 FASE 3: IMPLEMENTAR FUNCIONALIDAD CORE FALTANTE (Semana 2 — Prioridad 🔴)

### Task F3.1: Implementar Upload Real de Archivos (AC-004)
**Archivos:** `app/routers/reportes.py`, `app/models.py`, `src/frontend/src/components/ReportForm.jsx`
**Cambios:**
1. Endpoint POST `/api/reportes/upload` con `python-multipart`
2. Procesamiento: strip EXIF (Pillow), thumbnail, rename aleatorio, encriptación AES-256-GCM
3. `<input type="file" multiple>` con drag & drop en frontend
4. Preview de imagen antes de enviar
5. Validación: tipo (jpg, png, mp4, mp3), tamaño (max 10MB)

**DoD:**
- [ ] Endpoint funciona (test con curl)
- [ ] Archivo se encripta y almacena
- [ ] EXIF se elimina
- [ ] Thumbnail se genera
- [ ] Tests de integración pasan
- [ ] Linter pasa
- [ ] Commit: `feat(PROYECTO-005): implementa upload de evidencia multimedia`

### Task F3.2: Honeypot Field (AC-007)
**Archivos:** `src/frontend/src/components/ReportForm.jsx`, `app/routers/reportes.py`
**Cambios:**
1. Añadir campo invisible `<input name="website" style="display:none">` en frontend
2. Validación en backend: si campo no está vacío → retornar 400 (bot detectado)
3. Test: enviar con honeypot lleno → 400

**DoD:**
- [ ] Campo invisible en frontend
- [ ] Validación en backend
- [ ] Test pasa
- [ ] Commit: `feat(PROYECTO-005): añade honeypot anti-spam`

### Task F3.3: Review Step + Copiar Hash (AC-008)
**Archivos:** `src/frontend/src/components/ReportForm.jsx`
**Cambios:**
1. Añadir pantalla de "Revisar antes de enviar" que muestra resumen
2. Botón "Confirmar y enviar" solo en review step
3. Botón "Copiar hash al portapapeles" en pantalla de confirmación
4. Usar `navigator.clipboard.writeText()`

**DoD:**
- [ ] Review step visible
- [ ] Botón copiar funciona
- [ ] Tests E2E pasan
- [ ] Commit: `feat(PROYECTO-005): añade review step y copiar hash`

---

## 🎯 FASE 4: INFRAESTRUCTURA + DOCUMENTACIÓN (Semana 3 — Prioridad 🟡)

### Task F4.1: Completar Docker Compose (AC-006)
**Archivos:** `docker-compose.yml`, `Dockerfile`, `nginx.conf`
**Cambios:**
1. Añadir servicio `postgres:16` con volumen persistente
2. Añadir servicio `redis:7` para rate limiting
3. Añadir servicio `nginx` con `access_log off` para `/api/reportes`
4. Convertir Dockerfile a multi-stage (builder + runtime)
5. Configurar TLS 1.3 con Let's Encrypt (staging)

**DoD:**
- [ ] `docker-compose up` levanta todos los servicios
- [ ] App conecta a PostgreSQL
- [ ] Rate limiting usa Redis
- [ ] Nginx sirve frontend con access_log off
- [ ] Commit: `feat(PROYECTO-005): añade PostgreSQL, Redis, Nginx a docker-compose`

### Task F4.2: Documentación de Avances (AC-009)
**Archivos:** Nuevos
**Cambios:**
1. Crear `docs/LECCIONES-001.md` — Lecciones aprendidas del Módulo 001
2. Crear `docs/BITACORA-001.md` — Bitácora de avances (fecha, horas, lo que se hizo, bloqueos)
3. Crear `.github/pull_request_template.md` — Template de PR

**DoD:**
- [ ] Documentos creados y commiteados
- [ ] Commit: `docs(PROYECTO-005): añade lecciones, bitácora y template de PR`

### Task F4.3: AAD en Encriptación (AC-010)
**Archivos:** `app/services/encryption.py`
**Cambios:**
1. Añadir `associated_data=b"proteccion-infantil-v1"` a `aesgcm.encrypt` y `aesgcm.decrypt`
2. Test: encriptar y desencriptar con AAD funciona

**DoD:**
- [ ] AAD añadido
- [ ] Tests pasan
- [ ] Commit: `feat(PROYECTO-005): añade AAD a encriptación AES-256-GCM`

---

## 🎯 FASE 5: SOLICITAR VALIDACIÓN DE ZEUS

Cuando termines TODAS las fases anteriores:

1. **Crea PR** desde tu rama de corrección a `main`
2. **Asegúrate de que:**
   - Todos los tests pasan (GitHub Actions verde)
   - Cobertura ≥ 80%
   - Linter pasa
   - No hay dependencias fantasmas
3. **Escribe en la descripción del PR:**
   ```markdown
   ## Corrección Módulo 001
   
   - Fixes: AC-001 a AC-010 (ver docs/auditoria/ACTA-CORRECCION-ODIN-001.md)
   - Tests: Todos pasan
   - Cobertura: 80%+
   - Linter: Pasa
   
   @ZEUS — Solicito validación. Módulo 001 listo para revisión.
   ```
4. **Asigna a ZEUS como reviewer**
5. **Espera validación** — No declares "completado" hasta que ZEUS firme Acta de Validación

---

## 📊 TIMELINE SUGERIDO

| Semana | Fases | Horas | Entregable |
|--------|-------|-------|------------|
| 1 (Jun 15-21) | Fase 1 + Fase 2 | 18h | Fix estado + bugs críticos de seguridad |
| 2 (Jun 22-28) | Fase 3 | 20h | Upload real + honeypot + review step |
| 3 (Jun 29-Jul 5) | Fase 4 + Fase 5 | 12h | Infraestructura + docs + solicitud de validación |
| **Total** | | **50h** | Módulo 001 realmente completado |

---

## 📌 NOTAS FINALES

1. **No inventes funcionalidades.** Si no está en el spec, no lo hagas.
2. **No ignores los tests.** Si un test falla, el código no está listo.
3. **No declares "completado" sin DoD.** ZEUS rechazará si falta un check.
4. **El repo es la verdad.** Si no está commiteado, no existe.
5. **Pregunta si tienes dudas.** Mejor preguntar que asumir.

---

> **"Corregir es parte del proceso. La calidad es el resultado."**
> **ZEUS — CEO PMO, Innovadataco** ⚡
