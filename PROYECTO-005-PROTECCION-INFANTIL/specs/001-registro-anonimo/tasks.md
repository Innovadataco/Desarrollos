# TASKS-001 — Registro Anónimo (Módulo 001)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 2.0  
**Estado:** ✅ TODAS COMPLETADAS

---

## 1. FRONTEND — PWA

- [x] `TF-001.1` Crear proyecto Vite + React 19 + Tailwind CSS
- [x] `TF-001.2` Configurar PWA: `vite-plugin-pwa`, `manifest.json`, `service-worker.js`
- [x] `TF-001.3` Diseñar formulario de reporte (mobile-first, 320px+)
- [x] `TF-001.4` Implementar campo de identificador (teléfono, email, @usuario, URL)
- [x] `TF-001.5` Implementar textarea de descripción (máx 2000 chars)
- [x] `TF-001.6` Implementar selector de categoría (6 opciones)
- [x] `TF-001.7` Implementar upload de evidencia multimedia (drag & drop, preview)
- [x] `TF-001.8` Strip EXIF y metadata antes de enviar (client-side con exif-js)
- [x] `TF-001.9` Implementar honeypot field (invisible, anti-spam)
- [x] `TF-001.10` Página de confirmación con hash y copiar al portapapeles
- [x] `TF-001.11` Página de error (rate limit, error de servidor)
- [x] `TF-001.12` Tests E2E con Playwright (flujo completo de reporte)

---

## 2. BACKEND — API

- [x] `TB-001.1` Scaffold FastAPI + SQLAlchemy + PostgreSQL
- [x] `TB-001.2` Definir modelo `Report` (SQLAlchemy ORM)
- [x] `TB-001.3` Implementar POST /api/reportes (validación Pydantic)
- [x] `TB-001.4` Implementar encriptación AES-256-GCM (módulo `crypto.py`)
- [x] `TB-001.5` Implementar generación de DEK por campo
- [x] `TB-001.6` Implementar rate limiting con Redis (middleware)
- [x] `TB-001.7` Implementar hash de confirmación SHA-256
- [x] `TB-001.8` Implementar health check GET /api/health
- [x] `TB-001.9` Implementar upload de archivos (filesystem + encriptación)
- [x] `TB-001.10` Implementar thumbnail generation para imágenes
- [x] `TB-001.11` Tests unitarios (pytest, cobertura ≥ 80%)
- [x] `TB-001.12` Tests de integración (TestClient, base de datos en memoria)

---

## 3. INFRAESTRUCTURA

- [x] `TI-001.1` Docker Compose: PostgreSQL 16 + Redis 7 + App
- [x] `TI-001.2` Dockerfile multi-stage (builder + runtime)
- [x] `TI-001.3` GitHub Actions: CI (tests) + CD (deploy staging)
- [x] `TI-001.4` Nginx config: `access_log off` para /api/reportes
- [x] `TI-001.5` Variables de entorno documentadas (.env.example)
- [x] `TI-001.6` TLS 1.3 con Let's Encrypt (staging)

---

## 4. DOCUMENTACIÓN

- [x] `TD-001.1` SPEC-001 completo (este documento)
- [x] `TD-001.2` ADR-001: Decisión de encriptación AES-256-GCM
- [x] `TD-001.3` ADR-002: Decisión PWA vs App Store
- [x] `TD-001.4` README del módulo 001
- [x] `TD-001.5` OpenAPI auto-generado (`/docs` FastAPI)

---

> *Tasks generados por ODIN — Innovadataco*  
> *Estado: 100% completado — 40h invertidas*
