# Commit Convention — Innovadataco
**Versión:** 1.0.0  
**Basado en:** Conventional Commits 1.0.0  
**Herramienta:** ODIN (automatizado) + ZEUS (revisión)

---

## 1. FORMATO

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Ejemplo
```
feat(reportes): agregar endpoint POST /api/reportes

- Implementa creación de reportes anónimos
- Agrega encriptación AES-256-GCM
- Incluye rate limiting 5 req/hr/IP

Closes #123
```

---

## 2. TYPES

| Type | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva feature | `feat(auth): agregar login con OAuth2` |
| `fix` | Bug fix | `fix(reportes): corregir validación de email` |
| `docs` | Documentación | `docs(api): actualizar OpenAPI spec` |
| `style` | Formato (sin cambio de lógica) | `style: aplicar black a models.py` |
| `refactor` | Refactorización | `refactor(db): migrar a SQLAlchemy 2.0` |
| `test` | Tests | `test(reportes): agregar tests de integración` |
| `chore` | Tareas de mantenimiento | `chore: actualizar dependencias` |
| `security` | Seguridad | `security: rotar secrets, validar OWASP` |
| `perf` | Performance | `perf(db): agregar índice a report_hash` |
| `ci` | CI/CD | `ci: agregar GitHub Action para pytest` |

---

## 3. SCOPES

| Scope | Descripción |
|-------|-------------|
| `api` | Backend API (FastAPI) |
| `ui` | Frontend (React) |
| `db` | Base de datos / Modelos |
| `auth` | Autenticación / Autorización |
| `deploy` | Docker / CI/CD / Infra |
| `docs` | Documentación general |
| `security` | Seguridad / Encriptación |
| `pm2` | Artefactos PM2 (ZEUS) |

---

## 4. REGLAS

1. **Subject en español** (el proyecto es en español)
2. **Máximo 72 caracteres** en la línea de subject
3. **Body opcional** pero obligatorio para commits complejos (> 10 líneas)
4. **Footer para referencias:** `Closes #123`, `Refs #456`
5. **Breaking changes:** `BREAKING CHANGE: descripción` en footer
6. **Nunca:** `wip`, `temp`, `fix`, `asdf` como subject

---

## 5. EJEMPLOS POR PROYECTO

### Proyecto 005 (Protección Infantil)
```
feat(reportes): implementar módulo de registro anónimo

- POST /api/reportes con validación
- Encriptación AES-256-GCM de datos sensibles
- Rate limiting por IP
- Tests pytest 100% cobertura

Closes #5
```

```
security(encryption): rotar clave KEK y re-encriptar datos

- Nueva clave generada con openssl rand -hex 32
- Migración de datos con script one-off
- Backup de BD antes de migración

Refs #12, #15
BREAKING CHANGE: requiere nueva variable REPORT_ENCRYPTION_KEY
```

---

> "Un buen commit cuenta una historia. Un mal commit deja deuda técnica."
