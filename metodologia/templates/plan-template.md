# PLAN-{ID}: {NOMBRE DEL PLAN TÉCNICO}
## Proyecto: {PROYECTO-ID} — {NOMBRE PROYECTO}
**Versión:** 1.0.0  
**Fecha:** {YYYY-MM-DD}  
**Autor:** ODIN (CEO IA Dev)  
**Aprobador:** Jelkin (CEO)  
**Estado:** Borrador / En revisión / Aprobado

---

## 1. STACK TECNOLÓGICO

| Capa | Tecnología | Versión | Justificación |
|------|-----------|---------|---------------|
| Frontend | {React/Vue/Next.js} | {X.Y.Z} | {Por qué} |
| Backend | {FastAPI/Node/Express} | {X.Y.Z} | {Por qué} |
| Base de datos | {PostgreSQL/MySQL/Mongo} | {X.Y} | {Por qué} |
| Cache | {Redis} | {X.Y.Z} | {Por qué} |
| Auth | {OAuth2/JWT/bcrypt} | {X.Y.Z} | {Por qué} |
| Tests | {pytest/vitest/playwright} | {X.Y.Z} | {Por qué} |
| Deploy | {Docker/VPS/AWS} | {X.Y.Z} | {Por qué} |

---

## 2. ARQUITECTURA DE ALTO NIVEL

```
{Diagrama textual ASCII o link a imagen}

Ejemplo:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────►│   Backend   │────►│   Base de   │
│  (React)    │     │  (FastAPI)  │     │   Datos     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Redis     │
                    │  (Cache)    │
                    └─────────────┘
```

---

## 3. MODELO DE DATOS

### Entidades principales

| Entidad | Descripción | Campos clave |
|---------|-------------|--------------|
| {Entidad1} | {Descripción} | id, campo1, campo2, created_at |
| {Entidad2} | {Descripción} | id, campo1, campo2, entidad1_id |

### Diagrama ER (texto o link)

```
{Entidad1} ||--o{ {Entidad2} : tiene
{Entidad2} ||--o{ {Entidad3} : pertenece
```

---

## 4. API ENDPOINTS

### Módulo: {Nombre}

| Método | Ruta | Request | Response | Auth | Rate Limit |
|--------|------|---------|----------|------|------------|
| POST | /api/{recurso} | `{json}` | `{json}` | JWT | 5/hr |
| GET | /api/{recurso}/{id} | — | `{json}` | JWT | 100/hr |
| PUT | /api/{recurso}/{id} | `{json}` | `{json}` | JWT | 100/hr |
| DELETE | /api/{recurso}/{id} | — | `{json}` | JWT | 50/hr |

### Documentación OpenAPI
- URL dev: `http://localhost:8000/docs`
- URL prod: `{URL}/docs`

---

## 5. PLAN DE SEGURIDAD

### 5.1 Autenticación
- {OAuth2 / JWT / API Keys}
- {Flujo de login, refresh tokens, logout}

### 5.2 Autorización
- {Roles: admin, user, auditor}
- {RBAC / ABAC}

### 5.3 Encriptación
- {En reposo: AES-256-GCM}
- {En tránsito: TLS 1.3}

### 5.4 OWASP Top 10
- [ ] SQL Injection (ORM parametrizado)
- [ ] XSS (React escapa automático)
- [ ] CSRF (tokens en forms)
- [ ] Rate Limiting (slowapi / nginx)
- [ ] Secrets management (env vars, no hardcode)
- [ ] Dependency audit (npm audit, pip-audit)

---

## 6. ESTRATEGIA DE TESTING

| Tipo | Herramienta | Cobertura | Responsable |
|------|-------------|-----------|-------------|
| Unitario | pytest / vitest | 80% | ODIN |
| Integración | TestClient / Playwright | 100% endpoints | ODIN |
| E2E | Playwright | Flujos críticos | ODIN + ZEUS |
| Seguridad | OWASP ZAP / Burp | High/Medium | ZEUS |
| Performance | k6 / Locust | Latencia < 200ms | ODIN |

---

## 7. ESTRATEGIA DE DEPLOY

### 7.1 Entornos
- **Dev:** Local (Docker Compose)
- **Staging:** VPS / Cloud (Docker)
- **Prod:** VPS / Cloud (Docker + SSL)

### 7.2 CI/CD Pipeline (GitHub Actions)
```yaml
1. Push a feature/XXX
2. Run tests (pytest + vitest)
3. Run linter (ruff + black + eslint)
4. Run security audit (pip-audit + npm audit)
5. Build Docker image
6. Deploy to staging (auto)
7. Manual approval for prod
8. Deploy to prod
```

### 7.3 Rollback
- {Estrategia: tag de release, Docker image versionada, DB migrations reversibles}

---

## 8. ESTIMACIÓN DE ESFUERZO

| Fase | Tareas | Horas estimadas | Dependencias |
|------|--------|-----------------|--------------|
| Setup | {Tareas} | {X}h | Ninguna |
| Backend | {Tareas} | {X}h | Setup |
| Frontend | {Tareas} | {X}h | Backend API |
| Tests | {Tareas} | {X}h | Backend + Frontend |
| Deploy | {Tareas} | {X}h | Todo lo anterior |
| **Total** | | **{X}h** | |

---

> Generado por ODIN — Innovadataco
