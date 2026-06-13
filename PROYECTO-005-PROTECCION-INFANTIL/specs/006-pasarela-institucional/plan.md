# PLAN-006 — Pasarela Institucional (Módulo 006)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Planificado noviembre 2026

---

## 1. OBJETIVO

Implementar la pasarela institucional para envío de alertas a ICBF, Fiscalía, Policía y NCMEC, con formatos estándar, API gateway, y configuración de umbrales de alerta desde el panel admin.

---

## 2. TAREAS

| # | Tarea | Horas | Estado | Dependencia |
|---|-------|-------|--------|-------------|
| 6.1 | Implementar modelo `Institution` (SQLAlchemy) | 3h | ⬜ | — |
| 6.2 | Implementar modelo `Alert` (SQLAlchemy) | 3h | ⬜ | 6.1 |
| 6.3 | Implementar modelo `Digest` (SQLAlchemy) | 3h | ⬜ | 6.2 |
| 6.4 | Seed de instituciones (ICBF, Fiscalía, Policía, NCMEC) | 2h | ⬜ | 6.1 |
| 6.5 | Implementar envío de alerta por email (SMTP, estructurado) | 4h | ⬜ | 6.2 |
| 6.6 | Implementar formato JSON de exportación (estándar interno) | 3h | ⬜ | — |
| 6.7 | Implementar formato PDF de exportación (branding, reportlab) | 4h | ⬜ | 6.6 |
| 6.8 | Implementar formato NCMEC (CyberTipline API v2) | 4h | ⬜ | 6.6 |
| 6.9 | Implementar resumen de IA de 200 caracteres (para export) | 3h | ⬜ | 3.11 |
| 6.10 | Implementar alertas automáticas por severidad (cron job) | 4h | ⬜ | 6.5, 6.6 |
| 6.11 | Implementar digest diario, semanal, mensual (cron job) | 4h | ⬜ | 6.10 |
| 6.12 | Implementar API gateway con API key (auth institucional) | 4h | ⬜ | 5.1 |
| 6.13 | Implementar rate limiting 100 req/hr por institución | 2h | ⬜ | 6.12 |
| 6.14 | Implementar confirmación de recepción por institución | 3h | ⬜ | 6.12 |
| 6.15 | Panel admin: configuración de umbrales y destinatarios | 4h | ⬜ | 5.15 |
| 6.16 | Tests de integración con mock servers | 6h | ⬜ | — |
| 6.17 | ADR + documentación | 2h | ⬜ | — |
| **Total** | | **48h** | | |

---

## 3. HITOS

**Hito 6.1 (Nov 1-7):** Modelos + seed + email estructurado  
**Hito 6.2 (Nov 8-14):** Formatos JSON/PDF/NCMEC + resumen IA  
**Hito 6.3 (Nov 15-21):** Alertas automáticas + digest + cron jobs  
**Hito 6.4 (Nov 22-30):** API gateway + confirmación + panel admin + tests + documentación

---

## 4. DEPENDENCIAS

- Módulo 001 (Reporte) completado
- Módulo 002 (Consulta) completado
- Módulo 003 (IA Triage) completado
- Módulo 004 (Clustering) completado
- Módulo 005 (Panel Admin) completado
- PostgreSQL + Redis operativos
- SMTP configurado (SendGrid / AWS SES / Mailgun)

---

## 5. RIESGOS

| Riesgo | Mitigación |
|--------|------------|
| Institución no tiene API | Email estructurado como fallback universal |
| Email bloqueado por spam | SPF, DKIM, DMARC configurados. Whitelist de dominios. |
| NCMEC rechaza formato | Validar schema contra especificación NCMEC v2 antes de enviar |
| Latencia de alerta alta | Email inmediato + API gateway async + retry 3x con backoff |
| Institución no confirma recepción | Alerta se marca como "delivered" al enviar email con read receipt |

---

> *Plan generado por ZEUS — Innovadataco*
