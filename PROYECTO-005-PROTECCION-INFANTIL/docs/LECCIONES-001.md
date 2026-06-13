# LECCIONES-001 — Correcciones tras auditoría ZEUS al Módulo 001

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio de 2026  
**Autor:** ODIN  
**Estado:** Borrador abierto

---

## 1. Contexto

La auditoría ZEUS de la rama `setup/estructura-2026` identificó que el Módulo 001 (Registro Anónimo) fue declarado **COMPLETADO** al 65 % aproximadamente, con varios ítems marcados como terminados que no estaban reflejados en código o que presentaban defectos críticos.

Este documento registra las lecciones aprendidas y las decisiones tomadas para evitar que vuelva a repetirse en los módulos siguientes.

---

## 2. Lecciones aprendidas

### 2.1 No declarar "completado" sin evidencia verificable

- **Problema:** El estado `✅ COMPLETADO` apareció en `spec.md`, `plan.md`, `tasks.md` y `README.md` sin Acta de Validación firmada por ZEUS.
- **Impacto:** Deuda técnica crítica oculta, falsas expectativas de avance y riesgo de pasar a producción con funcionalidades inexistentes.
- **Decisión:** A partir de ahora ningún módulo podrá declararse `COMPLETADO` hasta que ZEUS emita un Acta de Validación. Los estados intermedios serán `🚧 en desarrollo` o `🚧 en corrección`.

### 2.2 Definition of Done (DoD) con checklist mínima

Cada tarea debe demostrar, como mínimo:

1. Código implementado y revisado.
2. Tests unitarios + integración con cobertura ≥ 80 %.
3. Linter/formatter sin advertencias (`ruff`, `black`, `eslint`, `prettier`).
4. Build de producción exitoso (backend + frontend).
5. Security checklist aplicada (rate limit, encriptación, validación, secrets).
6. Documentación actualizada (`spec.md`, ADR si aplica).
7. Commit con mensaje convencional (`feat:`, `fix:`, `docs:`, etc.).

### 2.3 Rate limiting: la IP nunca debe almacenarse en texto plano

- **Problema:** El limitador usaba `RateLimitItemPerMinute` y la IP sin hashear.
- **Impacto:** Fuga potencial de PII en logs o almacenamiento de Redis/memoria.
- **Decisión:** Se migra a `RateLimitItemPerHour(5)` para reportes y se hashea la IP con SHA-256 antes de usarla como clave.

### 2.4 Modelo de datos debe reflejar el SPEC desde el primer día

- **Problema:** Faltaban campos como `category`, `consent_location`, `city`, `country`; el timestamp tenía precisión completa.
- **Impacto:** Imposible cumplir los requisitos de anonimato y categorización.
- **Decisión:** Se añaden los campos y se trunca `reported_at` a un bucket de 6 horas (`reported_at_bucket`).

### 2.5 Anti-spam requiere honeypot + validación server-side

- **Problema:** No existía honeypot; cualquier bot podía inundar el endpoint.
- **Decisión:** Campo invisible `website` en frontend; rechazo silencioso en backend con registro en audit log.

### 2.6 UX de confirmación: copiar hash y revisar antes de enviar

- **Problema:** No había paso de revisión ni botón para copiar el hash.
- **Decisión:** El wizard pasa a 4 pasos (tipo → datos → evidencia → revisión) y se añade botón "Copiar código".

### 2.7 Evidencia multimedia: strip EXIF + thumbnail + encriptación

- **Problema:** Los adjuntos se guardaban sin procesar y sin encriptar.
- **Decisión:** Pipeline de evidencia: validación → strip EXIF → thumbnail → encriptación AES-256-GCM con DEK por archivo.

### 2.8 Infraestructura como código desde el inicio

- **Problema:** `docker-compose.yml` no incluía PostgreSQL, Redis ni Nginx.
- **Decisión:** Compose completo con `postgres:16`, `redis:7`, `nginx`, `access_log off` para `/api/reportes`, TLS 1.3 documentado y Dockerfiles multi-stage.

---

## 3. Checklist de prevención para próximos módulos

- [ ] Especificar el DoD antes de escribir código.
- [ ] No marcar tareas completadas hasta tener tests verdes.
- [ ] Revisar seguridad antes de cada PR (ver `security-checklist.md` cuando exista).
- [ ] Actualizar `docs/BITACORA-XXX.md` en cada sesión de trabajo.
- [ ] Separar claramente el territorio de ZEUS (`docs/auditoria/`) del de ODIN (`src/`, `specs/`, `docs/` operativos).

---

> *Documento vivo: se actualiza a medida que se cierran deudas técnicas.*
