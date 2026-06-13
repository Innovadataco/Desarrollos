# PLAN-001: Plan Técnico — Registro Anónimo de Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-12  
**Autor:** ODIN (CEO IA Dev)  
**Aprobador:** Jelkin (CEO)  
**Estado:** Aprobado

---

## 1. STACK TECNOLÓGICO

| Capa | Tecnología | Versión | Justificación |
|------|-----------|---------|---------------|
| Frontend | React | 19.0.0 | Componentes reactivos, ecosistema maduro |
| Build tool | Vite | 6.0.0 | Rápido, HMR, soporte PWA |
| CSS | Tailwind CSS | 3.4.17 | Utility-first, prototipado rápido |
| Backend | FastAPI | 0.136.3 | Alto rendimiento, validación Pydantic, OpenAPI auto |
| ORM | SQLAlchemy | 2.0.50 | Mapeo objeto-relacional robusto |
| Base de datos | SQLite (dev) / PostgreSQL (prod) | - | SQLite sin infra en dev; PostgreSQL escalable en prod |
| Cache/Rate limit | Redis (prod) / Memoria (dev) | 4.0.0+ | Redis distribuido; memoria para desarrollo local |
| Encriptación | cryptography (AES-256-GCM) | 48.0.1 | Estándar industrial, disponible en Python |
| Tests backend | pytest + pytest-cov | 9.0.3 / 7.1.0 | Tests unitarios e integración con cobertura |
| Tests frontend | vitest + Testing Library | 3.0.0 | Tests de componentes React |
| Deploy | Docker + Uvicorn | - | Contenedores para prod/staging |

---

## 2. ARQUITECTURA DE ALTO NIVEL

```
┌─────────────────────────────────────────────────────────────────┐
│                         Usuario (navegador)                      │
│              Sin login, sin cookies, sin IP guardada             │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Frontend — React + Vite (http://localhost:5173)                 │
│  • ReportForm.jsx                                               │
│  • POST /api/reportes                                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │ CORS restringido
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Backend — FastAPI (http://localhost:8000)                       │
│  • Middleware de headers de seguridad                           │
│  • /api/reportes → validación, rate limit, encriptación, BD     │
│  • /api/health → health check                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │ SQLAlchemy ORM
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Base de datos — SQLite (dev) / PostgreSQL (prod)                │
│  Tabla: reports                                                 │
│  Campos sensibles encriptados con AES-256-GCM                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Redis (opcional en prod) — Rate limiting distribuido            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. MODELO DE DATOS

### Entidad: Report

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Primary key |
| report_hash | String(64), unique, index | Hash de confirmación único |
| reported_identifier | LargeBinary | Identificador encriptado |
| description | LargeBinary | Descripción encriptada |
| evidence_type | String(10), nullable | `text` o `image` |
| evidence_content | LargeBinary, nullable | Evidencia encriptada |
| reported_at | DateTime(timezone=True) | Fecha de creación |
| updated_at | DateTime(timezone=True) | Fecha de última actualización |

---

## 4. API ENDPOINTS

### Módulo: Reportes

| Método | Ruta | Request | Response | Auth | Rate Limit |
|--------|------|---------|----------|------|------------|
| POST | /api/reportes | `{"reported_identifier": "...", "description": "...", "evidence": {"type": "text", "content": "..."}}` | `{"report_hash": "...", "reported_at": "..."}` | Ninguna | 5/hr/IP |
| GET | /api/health | — | `{"status": "ok"}` | Ninguna | Ninguno |

### Documentación OpenAPI
- Dev: http://localhost:8000/docs
- Prod: `{URL}/docs`

---

## 5. PLAN DE SEGURIDAD

### 5.1 Autenticación
- No aplica para reportantes (sistema anónimo).
- Futuro panel de admin requerirá autenticación (módulo 002).

### 5.2 Autorización
- No aplica en este módulo.

### 5.3 Encriptación
- **Reposo:** AES-256-GCM con DEK aleatoria por campo y KEK derivada de `REPORT_ENCRYPTION_KEY`.
- **Tránsito:** TLS 1.3 en producción (configurar en reverse proxy).

### 5.4 OWASP Top 10
- [x] SQL Injection: SQLAlchemy ORM parametrizado.
- [x] XSS: React escapa automáticamente.
- [x] CSRF: No aplica (sin sesión/cookies).
- [x] Rate Limiting: 5 reportes/hora/IP.
- [x] Secrets: variables de entorno, sin hardcode.
- [x] Dependency audit: npm audit / pip-audit pendiente en CI.
- [x] Headers de seguridad: HSTS, CSP, X-Frame, etc.

---

## 6. ESTRATEGIA DE TESTING

| Tipo | Herramienta | Cobertura | Responsable |
|------|-------------|-----------|-------------|
| Unitario backend | pytest | ≥ 80% | ODIN |
| Integración backend | TestClient (FastAPI) | 100% endpoints | ODIN |
| Unitario frontend | vitest + Testing Library | Componentes críticos | ODIN |
| Seguridad | OWASP ZAP | Antes de prod | ZEUS |

---

## 7. ESTRATEGIA DE DEPLOY

### 7.1 Entornos
- **Dev:** Local con SQLite y memoria.
- **Staging:** Docker + PostgreSQL + Redis.
- **Prod:** Docker + PostgreSQL + Redis + TLS.

### 7.2 Variables de entorno críticas
- `DATABASE_URL`
- `REPORT_ENCRYPTION_KEY` (64 hex chars)
- `ENVIRONMENT`
- `REDIS_URL` (opcional)

### 7.3 Rollback
- Tags de release en Git.
- Backups de BD antes de migraciones.
- Imágenes Docker versionadas.

---

## 8. ESTIMACIÓN DE ESFUERZO

| Fase | Tareas | Horas estimadas | Dependencias |
|------|--------|-----------------|--------------|
| Setup | Estructura, dependencias, .env | 4h | Ninguna |
| Backend | API, modelos, encriptación, rate limit | 16h | Setup |
| Frontend | Formulario, validación, UX | 8h | Backend API |
| Tests | pytest + vitest + cobertura | 8h | Backend + Frontend |
| Docs | SDD: spec, plan, tasks, ADR | 4h | Todo lo anterior |
| **Total** | | **40h** | |

---

> Generado por ODIN — Innovadataco
