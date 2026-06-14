# PLAN-004 — Clustering y Perfil (Módulo 004)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Planificado septiembre 2026

---

## 1. OBJETIVO

Implementar clustering geográfico, generación de perfiles de contacto, y detección de redes organizadas, con privacidad y audit trail.

---

## 2. TAREAS

| # | Tarea | Horas | Estado | Dependencia |
|---|-------|-------|--------|-------------|
| 4.1 | Implementar geocodificación (MaxMind GeoLite2 local) | 6h | ⬜ | — |
| 4.2 | Implementar modelo `Profile` (SQLAlchemy) | 3h | ⬜ | TB-001.2 |
| 4.3 | Implementar modelo `ProfileUpdate` (audit trail) | 3h | ⬜ | 4.2 |
| 4.4 | Implementar algoritmo de clustering (criterios) | 4h | ⬜ | — |
| 4.5 | Implementar endpoint GET /api/profile/{hash} | 4h | ⬜ | 4.2 |
| 4.6 | Implementar endpoint GET /api/networks | 3h | ⬜ | 4.5 |
| 4.7 | Implementar recálculo automático de perfil al recibir reporte | 4h | ⬜ | 4.2, TB-003.4 |
| 4.8 | Implementar índice en identifier_hash | 2h | ⬜ | — |
| 4.9 | Implementar cache Redis de perfiles (TTL 1h) | 3h | ⬜ | — |
| 4.10 | Implementar cálculo de timeline (mes/año) | 4h | ⬜ | — |
| 4.11 | Implementar detección de red organizada (2+ criterios) | 4h | ⬜ | 4.4 |
| 4.12 | Tests unitarios + integración | 8h | ⬜ | — |
| 4.13 | Panel admin: visualización de perfiles y redes | 6h | ⬜ | 4.5 |
| 4.14 | ADR-004 + documentación | 2h | ⬜ | — |
| **Total** | | **54h** | | |

---

## 3. HITOS

**Hito 4.1 (Sep 1-7):** Geocodificación + modelos de datos  
**Hito 4.2 (Sep 8-14):** Algoritmo + endpoints + recálculo automático  
**Hito 4.3 (Sep 15-21):** Cache + timeline + detección de redes  
**Hito 4.4 (Sep 22-30):** Panel admin + tests + documentación

---

## 4. DEPENDENCIAS

- Módulo 001 (Reporte) completado
- Módulo 002 (Consulta) completado
- Módulo 003 (IA Triage) completado (necesita scores para perfil)
- PostgreSQL + Redis operativos

---

## 5. RIESGOS

| Riesgo | Mitigación |
|--------|------------|
| Geocodificación imprecisa | MaxMind GeoLite2 local, sin API externa. Solo ciudad/país. |
| Escalabilidad con muchos reportes | Índice + cache Redis + recálculo lazy |
| Falso positivo de red organizada | 2+ criterios requeridos, no solo ciudades |
| Fuga de IP | Hashear y descartar inmediatamente |
| Perfil con datos identificables | Solo hash, nunca identificador real. Solo agregados. |

---

> *Plan generado por ZEUS — Innovadataco*
