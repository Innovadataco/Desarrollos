# TAREAS-005 — Módulo 005: Panel Admin
**Proyecto:** Semáforo de Confianza (005)
**Módulo activo:** 005 — Panel Admin
**Instrucción:** INSTRUCCION-ODIN-004-EXCEPCION.md
**Autorizado por:** Jelkin Carrillo (CEO)
**Fecha:** 2026-06-15
**Autor:** ZEUS (CEO PMO)

---

## 📋 LISTA DE TAREAS (26 items)

### 1. AUTENTICACIÓN (Backend)

- [ ] `TA-005.1` — Implementar modelo `User` (SQLAlchemy: username, password_hash, role, 2fa_secret, active)
- [ ] `TA-005.2` — Implementar endpoint POST /api/auth/login (bcrypt + JWT)
- [ ] `TA-005.3` — Implementar endpoint POST /api/auth/refresh (refresh token)
- [ ] `TA-005.4` — Implementar endpoint POST /api/auth/logout (blacklist JWT en Redis)
- [ ] `TA-005.5` — Implementar 2FA TOTP (setup y verify, opcional por usuario)
- [ ] `TA-005.6` — Implementar middleware de autenticación JWT
- [ ] `TA-005.7` — Implementar middleware de autorización por rol
- [ ] `TA-005.8` — Implementar rate limiting en login (5 intentos / 15 min)
- [ ] `TA-005.9` — Seed de admin root (configurado por variable de entorno al primer deploy)

### 2. DASHBOARD (Frontend + Backend)

- [ ] `TF-005.1` — Página de login (UI minimalista, mobile-first)
- [ ] `TF-005.2` — Dashboard: cards de métricas (reportes hoy, semana, mes)
- [ ] `TF-005.3` — Dashboard: gráfico de semáforo (doughnut chart)
- [ ] `TF-005.4` — Dashboard: lista de alertas (critical sin revisar)
- [ ] `TF-005.5` — Dashboard: tendencia de reportes (gráfico de línea, 30 días)
- [ ] `TF-005.6` — Endpoint GET /api/admin/dashboard (aggregations SQL)

### 3. REPORTES (Frontend + Backend)

- [ ] `TF-005.7` — Página de lista de reportes: tabla con filtros laterales
- [ ] `TF-005.8` — Paginación (20 por página)
- [ ] `TF-005.9` — Filtros: fecha, score, nivel, categoría, estado, ciudad, país
- [ ] `TF-005.10` — Ordenamiento: fecha, score, nivel
- [ ] `TF-005.11` — Página de detalle de reporte: metadata, botón desencriptar
- [ ] `TF-005.12` — Modal de desencriptar: input de razón (20 chars mínimo)
- [ ] `TF-005.13` — Visualización de contenido desencriptado (texto + evidence)
- [ ] `TF-005.14` — Cambio de estado: dropdown + notas
- [ ] `TF-005.15` — Endpoint GET /api/admin/reports (con filtros, paginación)
- [ ] `TF-005.16` — Endpoint GET /api/admin/reports/{id}
- [ ] `TF-005.17` — Endpoint POST /api/admin/reports/{id}/decrypt
- [ ] `TF-005.18` — Endpoint PATCH /api/admin/reports/{id}/status
- [ ] `TF-005.19` — Endpoint GET /api/admin/reports/{id}/audit (historial de acciones)

### 4. AUDIT TRAIL (Backend + Frontend)

- [ ] `TB-005.1` — Implementar modelo `AuditLog` (SQLAlchemy)
- [ ] `TB-005.2` — Registrar login/logout automáticamente
- [ ] `TB-005.3` — Registrar desencriptación (con razón, report_id, admin_id)
- [ ] `TB-005.4` — Registrar cambio de estado (con notas, old_status, new_status)
- [ ] `TB-005.5` — Registrar export (con filtros, formato, cantidad de registros)
- [ ] `TB-005.6` — Registrar visualización de perfil
- [ ] `TB-005.7` — Endpoint GET /api/admin/audit (solo admin+, con filtros)
- [ ] `TB-005.8` — Página de audit trail (solo admin+, tabla con filtros)

### 5. EXPORT (Backend + Frontend)

- [ ] `TB-005.9` — Implementar export JSON (schema fijo, datos encriptados o desencriptados según flag)
- [ ] `TB-005.10` — Implementar export PDF (reportlab o weasyprint, branding Innovadataco)
- [ ] `TB-005.11` — Endpoint POST /api/admin/export (JSON)
- [ ] `TB-005.12` — Endpoint POST /api/admin/export/pdf (PDF, async, email cuando listo)
- [ ] `TF-005.20` — UI de export: selección de filtros, formato, preview de cantidad

### 6. CONFIGURACIÓN (Frontend + Backend)

- [ ] `TF-005.21` — Página de configuración de umbrales de alerta (solo supervisor+)
- [ ] `TF-005.22` — Página de gestión de usuarios (solo admin+): crear, editar rol, desactivar
- [ ] `TF-005.23` — Endpoint PATCH /api/admin/config/thresholds
- [ ] `TF-005.24` — Endpoint CRUD /api/admin/users (solo admin+)

### 7. TESTS

- [ ] `TT-005.1` — Tests E2E Playwright: login → dashboard → lista → detalle → desencriptar → cambio estado → logout
- [ ] `TT-005.2` — Tests unitarios auth (bcrypt, JWT, 2FA)
- [ ] `TT-005.3` — Tests unitarios de permisos (viewer no desencripta, reviewer sí)
- [ ] `TT-005.4` — Tests de integración de endpoints admin
- [ ] `TT-005.5` — Tests de audit trail (cada acción registrada)

### 8. DOCUMENTACIÓN

- [ ] `TD-005.1` — ADR: Decisión de auth JWT + roles + audit trail
- [ ] `TD-005.2` — Documentación de endpoints admin (api-reference.md)

---

> **Nota para ODIN:** Lee este archivo al inicio. Desarrolla las tareas marcadas como `[ ]`. Reporta progreso en `PROGRESO-005.md`. No marques `[x]` sin verificar que funciona.
