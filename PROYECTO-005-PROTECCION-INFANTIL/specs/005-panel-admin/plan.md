# PLAN-005 — Panel de Administración (Módulo 005)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Planificado octubre 2026

---

## 1. OBJETIVO

Implementar panel de administración seguro con autenticación JWT, desencriptación bajo demanda con audit trail, dashboard de métricas, y export de datos para autoridades.

---

## 2. TAREAS

| # | Tarea | Horas | Estado | Dependencia |
|---|-------|-------|--------|-------------|
| 5.1 | Implementar auth JWT (login, refresh, logout) | 6h | ⬜ | — |
| 5.2 | Implementar 2FA TOTP (opcional, setup por root) | 4h | ⬜ | 5.1 |
| 5.3 | Implementar modelo de roles (viewer, reviewer, supervisor, admin, root) | 4h | ⬜ | 5.1 |
| 5.4 | Implementar dashboard de métricas (endpoint + UI) | 6h | ⬜ | 5.1 |
| 5.5 | Implementar lista de reportes con filtros y paginación | 6h | ⬜ | 5.1, TB-001.2 |
| 5.6 | Implementar detalle de reporte (metadata, botón desencriptar) | 4h | ⬜ | 5.5 |
| 5.7 | Implementar desencriptación bajo demanda (con razón + límite) | 6h | ⬜ | 5.6, TB-001.4 |
| 5.8 | Implementar audit trail (AuditLog) | 4h | ⬜ | 5.7 |
| 5.9 | Implementar cambio de estado de reporte | 3h | ⬜ | 5.5 |
| 5.10 | Implementar export JSON (schema fijo) | 4h | ⬜ | 5.5 |
| 5.11 | Implementar export PDF (branding, formato institucional) | 4h | ⬜ | 5.10 |
| 5.12 | Panel admin: visualización de perfiles y redes (Módulo 004) | 6h | ⬜ | 4.13 |
| 5.13 | Tests E2E con Playwright (flujo completo admin) | 8h | ⬜ | — |
| 5.14 | Tests unitarios + integración | 4h | ⬜ | — |
| 5.15 | ADR + documentación | 2h | ⬜ | — |
| **Total** | | **50h** | | |

---

## 3. HITOS

**Hito 5.1 (Oct 1-7):** Auth + roles + dashboard  
**Hito 5.2 (Oct 8-14):** Lista de reportes + filtros + detalle  
**Hito 5.3 (Oct 15-21):** Desencriptación + audit trail + cambio de estado  
**Hito 5.4 (Oct 22-31):** Export + perfiles + tests + documentación

---

## 4. DEPENDENCIAS

- Módulo 001 (Reporte) completado
- Módulo 002 (Consulta) completado
- Módulo 003 (IA Triage) completado
- Módulo 004 (Clustering) completado
- PostgreSQL + Redis operativos

---

## 5. RIESGOS

| Riesgo | Mitigación |
|--------|------------|
| Brute force de passwords | Rate limiting login, bcrypt 12 rounds, bloqueo 15 min tras 5 intentos |
| JWT comprometido | Expiración 1h, refresh 24h, blacklist en Redis al logout |
| Admin descifra sin razón | Razón obligatoria (20 chars), límite 10/hr, audit trail |
| Evidence URL filtrada | Expira 5 min, token único, solo accesible con JWT válido |
| Escalación de privilegios | Roles estrictos, root solo configurado por deploy |

---

> *Plan generado por ZEUS — Innovadataco*
