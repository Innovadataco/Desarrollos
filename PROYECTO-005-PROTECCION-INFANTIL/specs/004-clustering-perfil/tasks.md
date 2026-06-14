# TASKS-004 — Clustering y Perfil (Módulo 004)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Pendientes

---

## 1. GEOPROCESAMIENTO

- [ ] `TCL-004.1` Descargar e integrar MaxMind GeoLite2 (local, sin API externa)
- [ ] `TCL-004.2` Implementar geocodificación: IP → ciudad/país aproximado
- [ ] `TCL-004.3` Implementar stripping de IP: hashear SHA-256, descartar inmediatamente
- [ ] `TCL-004.4` Guardar solo ciudad/país en `Report` (si `consent_location=true`)
- [ ] `TCL-004.5` Tests de geocodificación (fixtures con IPs conocidas)

## 2. MODELO DE DATOS

- [ ] `TB-004.1` Implementar modelo `Profile` (SQLAlchemy, tabla completa)
- [ ] `TB-004.2` Implementar modelo `ProfileUpdate` (audit trail)
- [ ] `TB-004.3` Crear índice B-tree en `identifier_hash`
- [ ] `TB-004.4` Migración de datos existentes (generar perfiles de reportes históricos)
- [ ] `TB-004.5` Trigger: al insertar reporte, recalcular perfil automáticamente

## 3. ALGORITMOS

- [ ] `TCL-004.6` Implementar algoritmo de clustering (criterios de red)
- [ ] `TCL-004.7` Implementar cálculo de timeline (agrupar por mes/año)
- [ ] `TCL-004.8` Implementar cálculo de score promedio y máximo
- [ ] `TCL-004.9` Implementar detección de categorías frecuentes
- [ ] `TCL-004.10` Implementar detección de tipos de evidencia únicos
- [ ] `TCL-004.11` Recálculo lazy: recalcular solo si TTL de Redis expiró

## 4. ENDPOINTS

- [ ] `TB-004.6` Implementar GET /api/profile/{identifier_hash} (solo admin)
- [ ] `TB-004.7` Implementar GET /api/networks (solo admin, lista de is_network=true)
- [ ] `TB-004.8` Implementar GET /api/profile/{hash}/timeline (solo admin)
- [ ] `TB-004.9` Implementar GET /api/profile/{hash}/updates (solo admin, audit trail)
- [ ] `TB-004.10` Middleware de autenticación admin para todos los endpoints de perfil

## 5. FRONTEND — PANEL ADMIN

- [ ] `TF-004.1` Página de perfiles: tabla con filtros (report_count, score, is_network)
- [ ] `TF-004.2` Página de detalle de perfil: timeline, categorías, evidencia, mapa (ciudades)
- [ ] `TF-004.3` Página de redes: lista de identificadores con flag is_network
- [ ] `TF-004.4` Visualización de mapa: ciudades del perfil (sin coordenadas exactas)
- [ ] `TF-004.5` Tests E2E con Playwright (panel admin)

## 6. INFRAESTRUCTURA

- [ ] `TI-004.1` Cache Redis para perfiles (clave: `profile:{hash}`, TTL 1h)
- [ ] `TI-004.2` Cache Redis para networks (clave: `networks:list`, TTL 15min)
- [ ] `TI-004.3` Background job para recálculo de perfiles (Redis queue + worker)

## 7. DOCUMENTACIÓN

- [ ] `TD-004.1` ADR-004: Decisión de algoritmo clustering + privacidad
- [ ] `TD-004.2` Documentación de endpoints de perfil (api-reference.md)

---

> *Tasks generados por ZEUS — Innovadataco*
