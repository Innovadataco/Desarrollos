# TASKS-002 — Consulta Semáforo (Módulo 002)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Pendientes

---

## 1. FRONTEND — PWA

- [ ] `TF-002.1` Crear página principal como buscador (no como reporte)
- [ ] `TF-002.2` Implementar input universal con placeholder dinámico
- [ ] `TF-002.3` Detectar tipo de identificador (teléfono, email, @, URL)
- [ ] `TF-002.4` Diseñar cards de semáforo (4 colores, animación suave)
- [ ] `TF-002.5` Implementar detalle de resultado (conteos, categorías, timeline)
- [ ] `TF-002.6` Implementar botón "Reportar este identificador" → pre-llena Módulo 001
- [ ] `TF-002.7` Implementar botón "Compartir resultado" (URL sin identificador)
- [ ] `TF-002.8` Implementar "Alertarme si cambia" (email, Premium)
- [ ] `TF-002.9` PWA: página principal como consulta (cambio de routing)
- [ ] `TF-002.10` Tests E2E con Playwright (flujo consulta + reporte)

---

## 2. BACKEND — API

- [x] `TB-002.1` Implementar endpoint GET /api/validate/{identifier}
- [x] `TB-002.2` Implementar normalización de identificadores (E.164, email, @, URL)
- [x] `TB-002.3` Implementar hash SHA-256 para búsqueda
- [ ] `TB-002.4` Implementar query agregada por identifier_hash
- [ ] `TB-002.5` Implementar algoritmo de semáforo (verde/amarillo/rojo/negro)
- [ ] `TB-002.6` Implementar rate limiting 10/hr para consulta
- [ ] `TB-002.7` Implementar respuesta que NO expone datos del reportante
- [ ] `TB-002.8` Tests unitarios (pytest, cobertura ≥ 80%)
- [ ] `TB-002.9` Tests de integración (TestClient, fixtures con datos)

---

## 3. INFRAESTRUCTURA

- [ ] `TI-002.1` Índice en `identifier_hash` (PostgreSQL)
- [ ] `TI-002.2` Cache de consultas frecuentes (Redis, TTL 1h)
- [ ] `TI-002.3` Nginx: cache de respuestas 200 para consultas repetidas (5 min)

---

> *Tasks generados por ZEUS — Innovadataco*
