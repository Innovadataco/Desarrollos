# PLAN-002 — Consulta Semáforo (Módulo 002)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Planificado julio 2026

---

## 1. OBJETIVO

Implementar el buscador universal de identificadores con el Semáforo de Confianza Comunitaria, como PWA funcional y API REST.

---

## 2. TAREAS

| # | Tarea | Horas | Estado | Dependencia |
|---|-------|-------|--------|-------------|
| 2.1 | Diseñar UI de consulta (página principal) | 4h | ⬜ | — |
| 2.2 | Implementar input universal (teléfono, email, @, URL) | 3h | ⬜ | — |
| 2.3 | Implementar normalización de identificadores | 4h | ⬜ | — |
| 2.4 | Implementar endpoint GET /api/validate/{identifier} | 3h | ⬜ | TB-001.2 |
| 2.5 | Implementar algoritmo de semáforo | 3h | ⬜ | — |
| 2.6 | Diseñar cards de resultado (verde/amarillo/rojo/negro) | 4h | ⬜ | — |
| 2.7 | Implementar página de resultado con detalle | 4h | ⬜ | — |
| 2.8 | Implementar botón "Reportar" → Módulo 001 | 2h | ⬜ | TF-001.3 |
| 2.9 | Implementar rate limiting 10/hr para consulta | 2h | ⬜ | TB-001.6 |
| 2.10 | Tests unitarios + integración | 6h | ⬜ | — |
| 2.11 | PWA: página principal como consulta (no como reporte) | 2h | ⬜ | TF-001.2 |
| **Total** | | **36h** | | |

---

## 3. HITOS

**Hito 2.1 (Jul 1-5):** UI de consulta + normalización  
**Hito 2.2 (Jul 6-10):** API + algoritmo semáforo  
**Hito 2.3 (Jul 11-15):** Integración + tests + PWA  
**Hito 2.4 (Jul 16-20):** QA + ajustes + documentación

---

## 4. DEPENDENCIAS

- Módulo 001 (Registro Anónimo) completado
- Modelo `Report` con `identifier_hash` y `score` (parcial, Módulo 003 completa scoring)
- PostgreSQL + Redis operativos

---

## 5. RIESGOS

| Riesgo | Mitigación |
|--------|------------|
| Consulta lenta con muchos reportes | Índice en `identifier_hash`, query optimizada |
| Scraping de identificadores | Rate limiting 10/hr + CAPTCHA invisible si abuso |
| Stalking (buscar a alguien) | Sin información identificable del reportante, solo conteos agregados |

---

> *Plan generado por ZEUS — Innovadataco*
