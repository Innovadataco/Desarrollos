# PLAN-001 — Registro Anónimo (Módulo 001)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 2.0  
**Estado:** ✅ COMPLETADO

---

## 1. OBJETIVO

Implementar el formulario de reporte anónimo con evidencia multimedia, categorización de incidentes, y encriptación AES-256-GCM, como PWA funcional.

---

## 2. TAREAS COMPLETADAS

| # | Tarea | Horas | Estado |
|---|-------|-------|--------|
| 1.1 | Scaffold frontend React 19 + Vite + Tailwind | 4h | ✅ |
| 1.2 | Configurar PWA (manifest, service worker, Workbox) | 3h | ✅ |
| 1.3 | Formulario de reporte (3 campos + categoría) | 4h | ✅ |
| 1.4 | Upload de evidencia multimedia (drag & drop) | 4h | ✅ |
| 1.5 | Backend API POST /api/reportes | 3h | ✅ |
| 1.6 | Encriptación AES-256-GCM por campo | 4h | ✅ |
| 1.7 | Rate limiting con Redis | 2h | ✅ |
| 1.8 | Health check endpoint | 1h | ✅ |
| 1.9 | Tests unitarios + de integración | 6h | ✅ |
| 1.10 | Docker + Docker Compose | 3h | ✅ |
| 1.11 | Documentación SPEC + ADR-001 | 2h | ✅ |
| **Total** | | **40h** | ✅ |

---

## 3. HITOS Y DECISIONES

**Hito 1.1 (Jun 1-5):** Scaffold y PWA configurado  
**Hito 1.2 (Jun 6-10):** Formulario + upload funcional  
**Hito 1.3 (Jun 11-15):** Encriptación + API completa  
**Hito 1.4 (Jun 16-20):** Tests + Docker + documentación

**Decisiones clave:**
- ✅ PWA en lugar de App Store (ADR-002)
- ✅ AES-256-GCM con DEK por campo (ADR-001)
- ✅ Sin cookies, sin IP, sin tracking
- ✅ Evidencia multimedia: strip EXIF, thumbnail, encriptación
- ✅ Categorías de reporte para entrenamiento del modelo IA (Módulo 003)

---

## 4. DEPENDENCIAS

- Sin dependencias (primer módulo)
- PostgreSQL 16 disponible en Docker Compose
- Redis disponible en Docker Compose

---

## 5. RIESGOS MITIGADOS

| Riesgo | Mitigación | Estado |
|--------|------------|--------|
| Fuga de IP en logs | Nginx config: `access_log off` para /api/reportes | ✅ |
| Metadata en evidencia | Strip EXIF, rename archivo aleatorio | ✅ |
| Clave de encriptación expuesta | KEK en env var, nunca en código ni repo | ✅ |
| Spam/flood | Rate limiting 5/hr + honeypot field invisible | ✅ |

---

> *Plan generado por ODIN — Innovadataco*
