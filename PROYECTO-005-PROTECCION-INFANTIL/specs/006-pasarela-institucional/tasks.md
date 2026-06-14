# TASKS-006 — Pasarela Institucional (Módulo 006)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Pendientes

---

## 1. MODELOS DE DATOS

- [ ] `TB-006.1` Implementar modelo `Institution` (SQLAlchemy)
- [ ] `TB-006.2` Implementar modelo `Alert` (SQLAlchemy)
- [ ] `TB-006.3` Implementar modelo `Digest` (SQLAlchemy)
- [ ] `TB-006.4` Seed de instituciones en migración
- [ ] `TB-006.5` Generar API key por institución (bcrypt)
- [ ] `TB-006.6` Implementar rotación de API key (cada 3 meses, manual)

## 2. FORMATOS DE EXPORTACIÓN

- [ ] `TB-006.7` Implementar formato JSON estructurado (schema v1.0)
- [ ] `TB-006.8` Implementar formato PDF institucional (reportlab/weasyprint, branding)
- [ ] `TB-006.9` Implementar formato NCMEC CyberTipline v2 (XML)
- [ ] `TB-006.10` Implementar resumen de IA de 200 caracteres (para export, no texto original)
- [ ] `TB-006.11` Implementar thumbnail con marca de agua para PDF
- [ ] `TB-006.12` Implementar pie de página legal en PDF

## 3. ALERTAS

- [ ] `TB-006.13` Implementar envío de alerta por email (SMTP, async, Celery/Redis queue)
- [ ] `TB-006.14` Implementar email estructurado (HTML + JSON attachment)
- [ ] `TB-006.15` Implementar alerta automática por severidad (cron: severe inmediato, critical 4h, high 24h)
- [ ] `TB-006.16` Implementar alerta red organizada (siempre inmediato, sin importar score)
- [ ] `TB-006.17` Implementar retry con backoff exponencial (3 intentos)
- [ ] `TB-006.18` Implementar digest diario (cron: 08:00)
- [ ] `TB-006.19` Implementar digest semanal (cron: lunes 08:00)
- [ ] `TB-006.20` Implementar digest mensual (cron: primer día 08:00)
- [ ] `TB-006.21` Implementar panel admin: envío manual de alerta
- [ ] `TB-006.22` Implementar panel admin: generación manual de digest
- [ ] `TB-006.23` Implementar panel admin: configuración de umbrales y destinatarios
- [ ] `TB-006.24` Implementar panel admin: historial de alertas enviadas

## 4. API GATEWAY

- [ ] `TB-006.25` Implementar middleware de auth por API key (X-API-Key)
- [ ] `TB-006.26` Implementar rate limiting 100 req/hr por institución (Redis)
- [ ] `TB-006.27` Implementar endpoint POST /api/gateway/v1/reports
- [ ] `TB-006.28` Implementar endpoint POST /api/gateway/v1/digest
- [ ] `TB-006.29` Implementar endpoint POST /api/gateway/v1/confirm
- [ ] `TB-006.30` Implementar endpoint GET /api/gateway/v1/institutions (lista)
- [ ] `TB-006.31` TLS 1.3 obligatorio para gateway
- [ ] `TB-006.32` Audit trail de cada request en gateway (AuditLog)

## 5. TESTS

- [ ] `TT-006.1` Tests de integración con mock SMTP server
- [ ] `TT-006.2` Tests de integración con mock NCMEC API
- [ ] `TT-006.3` Tests de rate limiting de gateway (101ra request = 429)
- [ ] `TT-006.4` Tests de formato JSON (schema validation)
- [ ] `TT-006.5` Tests de formato PDF (generación correcta, no vacío)
- [ ] `TT-006.6` Tests de alerta automática por severidad (cron simulado)
- [ ] `TT-006.7` Tests de retry con backoff (fallo → éxito en 3er intento)
- [ ] `TT-006.8` Tests E2E con Playwright (panel admin: configuración de alertas)
- [ ] `TT-006.9` Tests unitarios ≥ 80% cobertura

## 6. DOCUMENTACIÓN

- [ ] `TD-006.1` ADR-005: Decisión de integración con autoridades
- [ ] `TD-006.2` Documentación de API gateway (api-reference.md)
- [ ] `TD-006.3` Manual de integración para instituciones (PDF)
- [ ] `TD-006.4` Schema de JSON de exportación (JSON Schema)

---

> *Tasks generados por ZEUS — Innovadataco*
