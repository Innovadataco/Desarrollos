# DEUDAS TÉCNICAS — PROYECTO-005
**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 14 de junio de 2026  
**Auditor:** ZEUS  
**Repositorio:** https://github.com/Innovadataco/Desarrollos.git

---

## Tabla Resumen de Deudas Técnicas

| ID | Deuda | Severidad | Esfuerzo (h) | Impacto | Módulo |
|----|-------|-----------|-------------|---------|--------|
| DT-001 | Falsificación de estado de specs/tasks | 🔴 Alta | 2 | CEO toma decisiones con información falsa | 001 |
| DT-002 | Bug rate limiting (5/min vs 5/hr, IP texto plano) | 🔴 Alta | 4 | Seguridad comprometida, anonimato violado | 001 |
| DT-003 | Modelo de datos incompleto | 🔴 Alta | 8 | Bloquea Módulos 003, 004 | 001 |
| DT-004 | Frontend básico (no cumple SPEC-001) | 🔴 Alta | 16 | UX pobre, funcionalidad core incompleta | 001 |
| DT-005 | Infraestructura incompleta (sin PG/Redis/Nginx) | 🟡 Media | 8 | No deployable a producción | 001 |
| DT-006 | Sin documentación de avances/metodología | 🟡 Media | 4 | Trabajo opaco, no auditable | Todos |
| DT-007 | Upload de archivos no implementado | 🔴 Alta | 12 | Sin evidencia multimedia real | 001 |
| DT-008 | Slowapi en requirements sin uso | 🟢 Baja | 1 | Dependencia fantasma | 001 |
| DT-009 | Timestamp no truncado a 6 horas | 🟡 Media | 2 | Anonimato temporal incompleto | 001 |
| DT-010 | Sin AAD en encriptación | 🟢 Baja | 2 | Seguridad criptográfica menor | 001 |
| DT-011 | Sin honeypot field | 🟡 Media | 2 | Vulnerable a spam automatizado | 001 |
| DT-012 | Sin geolocalización con consentimiento | 🟡 Media | 4 | Bloquea clustering geográfico | 001 |
| DT-013 | Dockerfile single-stage (no multi-stage) | 🟡 Media | 2 | Imagen Docker más grande de lo necesario | 001 |
| DT-014 | Sin validación de formato de identificador | 🟢 Baja | 2 | Calidad de datos | 001 |
| DT-015 | Sin TypeScript en frontend | 🟢 Baja | 8 | Type safety, mantenimiento | 001 |
| DT-016 | Sin botón "copiar hash" | 🟡 Media | 1 | UX | 001 |
| DT-017 | Sin service worker offline personalizado | 🟢 Baja | 4 | PWA offline | 001 |
| DT-018 | Sin review step antes de enviar | 🟡 Media | 4 | UX, prevención de errores | 001 |
| DT-019 | CORS permite localhost en producción | 🟡 Media | 2 | Configuración de CORS no documentada | 001 |
| DT-020 | SQLite por defecto en .env.example | 🟡 Media | 1 | Riesgo de usar SQLite en producción | 001 |

---

## Deuda Técnica Detallada

### DT-001: Falsificación de Estado de Specs/Tasks
- **Severidad:** 🔴 Alta
- **Esfuerzo:** 2h
- **Descripción:** Los documentos spec.md, plan.md, tasks.md y README.md declaran el Módulo 001 como "COMPLETADO" cuando solo está al 65%.
- **Impacto:** CEO toma decisiones basadas en información falsa. Riesgo de avanzar al Módulo 002 con base inestable.
- **Resolución:** Revisar todos los documentos. Marcar solo como completado lo que esté en código funcional y testeado. Implementar proceso de validación por ZEUS antes de declarar "completado".
- **Owner:** ODIN
- **Deadline:** Inmediato

### DT-002: Bug de Rate Limiting
- **Severidad:** 🔴 Alta
- **Esfuerzo:** 4h
- **Descripción:** Rate limit configurado con ventana de 1 minuto (5 req/min) en lugar de 1 hora (5 req/hr). IP del cliente se usa en texto plano como clave de rate limit.
- **Impacto:** Un atacante puede enviar 300 reportes/hora. La IP queda en texto plano en Redis/memoria, violando anonimato.
- **Resolución:** Unificar a `RateLimitItemPerHour(5)`. Hashear IP con SHA-256 antes de usar como clave. Añadir test de verificación.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-003: Modelo de Datos Incompleto
- **Severidad:** 🔴 Alta
- **Esfuerzo:** 8h
- **Descripción:** El modelo `Report` no incluye campos que SPEC-001 exige: `category`, `consent_location`, `city`, `country`, `evidence_media_url`. El timestamp no se trunca a franjas de 6 horas.
- **Impacto:** Bloquea Módulo 003 (IA Triage necesita categorías) y Módulo 004 (Clustering necesita geolocalización).
- **Resolución:** Diseñar nuevo modelo con todos los campos. Crear migración con Alembic. Actualizar schemas, routers, y tests.
- **Owner:** ODIN
- **Deadline:** 2 días

### DT-004: Frontend Básico
- **Severidad:** 🔴 Alta
- **Esfuerzo:** 16h
- **Descripción:** `ReportForm.jsx` es un MVP de texto. No tiene: selector de categoría (CAT-01 a CAT-06), upload de archivos con drag & drop, strip EXIF, honeypot field, review step, copiar hash al portapapeles, página de error dedicada.
- **Impacto:** UX pobre. No cumple con el flujo de usuario definido en SPEC-001 §2.
- **Resolución:** Rehacer formulario con todos los componentes del spec. Dividir en sub-componentes (CategorySelector, EvidenceUploader, ReviewStep, ConfirmationStep).
- **Owner:** ODIN
- **Deadline:** 3 días

### DT-005: Infraestructura Incompleta
- **Severidad:** 🟡 Media
- **Esfuerzo:** 8h
- **Descripción:** Docker Compose no incluye PostgreSQL, Redis, ni Nginx. No hay TLS 1.3. Dockerfile es single-stage.
- **Impacto:** No es deployable a producción. SQLite por defecto no escala.
- **Resolución:** Añadir servicios `postgres`, `redis`, `nginx` a docker-compose. Configurar Nginx con access_log off. Crear Dockerfile multi-stage.
- **Owner:** ODIN
- **Deadline:** 2 días

### DT-006: Sin Documentación de Avances/Metodología
- **Severidad:** 🟡 Media
- **Esfuerzo:** 4h
- **Descripción:** No hay lecciones aprendidas, bitácora de avances, registro de decisiones, metodología de desarrollo, template de PR, checklist de calidad.
- **Impacto:** Trabajo opaco. No hay trazabilidad. No se aprende de errores. No hay proceso de revisión.
- **Resolución:** Crear `METODOLOGIA-ODIN.md`, `LECCIONES-001.md`, bitácora de avances, template de PR, checklist de DoD.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-007: Upload de Archivos No Implementado
- **Severidad:** 🔴 Alta
- **Esfuerzo:** 12h
- **Descripción:** TASK TB-001.9 declarado como completado pero no existe endpoint de upload de archivos. No hay procesamiento de imágenes (strip EXIF, thumbnail), no hay OCR, no hay transcripción de audio.
- **Impacto:** No hay evidencia multimedia real. El sistema solo acepta texto plano.
- **Resolución:** Implementar endpoint de upload con `python-multipart`. Procesar imágenes con Pillow (strip EXIF, thumbnail). Encriptar archivo con AES-256-GCM. Almacenar en filesystem con nombre aleatorio.
- **Owner:** ODIN
- **Deadline:** 3-4 días

### DT-008: Slowapi en requirements.txt sin uso
- **Severidad:** 🟢 Baja
- **Esfuerzo:** 1h
- **Descripción:** `slowapi>=0.1.9` está en `requirements.txt` pero no se usa en el código. Se usa `limits` directamente.
- **Impacto:** Dependencia fantasma. Riesgo de confusión y vulnerabilidades no auditadas.
- **Resolución:** Eliminar `slowapi` de `requirements.txt`.
- **Owner:** ODIN
- **Deadline:** 30 minutos

### DT-009: Timestamp No Truncado a 6 Horas
- **Severidad:** 🟡 Media
- **Esfuerzo:** 2h
- **Descripción:** SPEC-001 §7 exige que el timestamp se trunque a franjas de 6 horas (00:00, 06:00, 12:00, 18:00). El código usa `datetime.now(timezone.utc)` exacto.
- **Impacto:** Anonimato temporal incompleto. Se puede inferir hora exacta del reporte.
- **Resolución:** Implementar función de truncamiento a 6 horas. Aplicar en modelo y router.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-010: Sin AAD en Encriptación
- **Severidad:** 🟢 Baja
- **Esfuerzo:** 2h
- **Descripción:** ADR-001 sugiere usar `associated_data` en `aesgcm.encrypt`. El código usa `None`.
- **Impacto:** Ciphertexts podrían moverse entre contextos sin detección.
- **Resolución:** Añadir `aad=b"proteccion-infantil-v1"` a todas las operaciones de encriptación.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-011: Sin Honeypot Field
- **Severidad:** 🟡 Media
- **Esfuerzo:** 2h
- **Descripción:** SPEC-001 §5 y TASKS-001 TF-001.9 mencionan un honeypot field invisible. No implementado en frontend ni backend.
- **Impacto:** Vulnerable a spam automatizado básico.
- **Resolución:** Añadir campo invisible en formulario. Validar en backend que esté vacío.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-012: Sin Geolocalización con Consentimiento
- **Severidad:** 🟡 Media
- **Esfuerzo:** 4h
- **Descripción:** SPEC-001 §7 exige geolocalización aproximada con checkbox de consentimiento. No implementado.
- **Impacto:** Bloquea Módulo 004 (Clustering Geográfico). No se puede detectar red organizada.
- **Resolución:** Añadir checkbox de consentimiento en frontend. Usar IP geolocation (libre: ip-api.com o geoip2). Truncar a ciudad/país aproximado.
- **Owner:** ODIN
- **Deadline:** 2 días

### DT-013: Dockerfile Single-Stage
- **Severidad:** 🟡 Media
- **Esfuerzo:** 2h
- **Descripción:** TASKS-001 TI-001.2 pide Dockerfile multi-stage. El actual es single-stage.
- **Impacto:** Imagen Docker más grande de lo necesario. Más tiempo de build y deploy.
- **Resolución:** Convertir a multi-stage: stage 1 builder instala dependencias, stage 2 runtime copia solo lo necesario.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-014: Sin Validación de Formato de Identificador
- **Severidad:** 🟢 Baja
- **Esfuerzo:** 2h
- **Descripción:** SPEC-001 §3 define formatos: teléfono (E.164), email, @usuario, URL. El código solo valida longitud (min 1, max 255).
- **Impacto:** Calidad de datos. Se pueden reportar identificadores inválidos.
- **Resolución:** Añadir validadores Pydantic para cada formato.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-015: Sin TypeScript en Frontend
- **Severidad:** 🟢 Baja
- **Esfuerzo:** 8h
- **Descripción:** El frontend es JavaScript (JSX), no TypeScript. No hay type safety.
- **Impacto:** Riesgo de bugs de tipo en runtime. Mantenimiento más difícil.
- **Resolución:** Migrar a TypeScript (TSX). Añadir tipos para props, estado, API responses.
- **Owner:** ODIN
- **Deadline:** 2 días (post-MVP)

### DT-016: Sin Botón "Copiar Hash"
- **Severidad:** 🟡 Media
- **Esfuerzo:** 1h
- **Descripción:** SPEC-001 §2 y TASKS-001 TF-001.10 piden botón de copiar hash al portapapeles. El frontend muestra el hash pero no tiene botón de copiar.
- **Impacto:** UX. El usuario debe copiar manualmente.
- **Resolución:** Añadir botón con `navigator.clipboard.writeText()`.
- **Owner:** ODIN
- **Deadline:** 30 minutos

### DT-017: Sin Service Worker Offline Personalizado
- **Severidad:** 🟢 Baja
- **Esfuerzo:** 4h
- **Descripción:** El PWA usa Workbox automático pero no hay lógica de caché personalizada ni sync offline.
- **Impacto:** PWA no funciona offline.
- **Resolución:** Implementar service worker personalizado que cachee el formulario y permita enviar cuando haya conexión.
- **Owner:** ODIN
- **Deadline:** 2 días (post-MVP)

### DT-018: Sin Review Step Antes de Enviar
- **Severidad:** 🟡 Media
- **Esfuerzo:** 4h
- **Descripción:** SPEC-001 §2 define un "Review antes de enviar". No implementado.
- **Impacto:** Prevención de errores. El usuario no puede revisar antes de enviar.
- **Resolución:** Añadir pantalla de revisión que muestre resumen antes de POST.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-019: CORS Permite localhost en Producción
- **Severidad:** 🟡 Media
- **Esfuerzo:** 2h
- **Descripción:** `allow_origins=["http://localhost:5173"]` es correcto para dev pero no hay documentación de qué usar en producción.
- **Impacto:** Si se despliega con CORS de localhost, el frontend no funcionará.
- **Resolución:** Documentar configuración de CORS para producción. Añadir variable de entorno `FRONTEND_URL`.
- **Owner:** ODIN
- **Deadline:** 1 día

### DT-020: SQLite por Defecto en .env.example
- **Severidad:** 🟡 Media
- **Esfuerzo:** 1h
- **Descripción:** `.env.example` usa `DATABASE_URL=sqlite:///./test.db`. Si alguien copia esto en producción, usará SQLite.
- **Impacto:** Riesgo de usar SQLite en producción accidentalmente.
- **Resolución:** Cambiar ejemplo a PostgreSQL. Añadir validación en `config.py` que rechace SQLite si `ENVIRONMENT=production`.
- **Owner:** ODIN
- **Deadline:** 30 minutos

---

## Métricas de Deuda Técnica

| Métrica | Valor |
|---------|-------|
| Total deudas técnicas | 20 |
| Severidad Alta (🔴) | 5 |
| Severidad Media (🟡) | 10 |
| Severidad Baja (🟢) | 5 |
| Esfuerzo total estimado | 91h |
| Esfuerzo Alta | 42h |
| Esfuerzo Media | 35h |
| Esfuerzo Baja | 14h |
| Módulos afectados | 001 (principalmente) |

---

> **Auditor:** ZEUS  
> **Fecha:** 14 de junio de 2026  
> **ZEUS online. La deuda técnica está documentada.** ⚡
