# Code Review Checklist — Innovadataco
**Versión:** 1.0.0  
**Responsable:** ZEUS (revisión) + ODIN (autocorrección)  
**Puente:** GitHub PRs

---

## 1. PROCESO DE CODE REVIEW

```
1. ODIN crea rama feature/XXX → implementa → tests pasan → push
2. ODIN crea PR en GitHub → asigna a ZEUS
3. ZEUS revisa contra spec.md + plan.md + PM2
4. ZEUS comenta en PR (aprobar, solicitar cambios, rechazar)
5. ODIN responde / corrige / justifica
6. ZEUS aprueba → Jelkin mergea (o auto-merge si configurado)
```

---

## 2. CHECKLIST DE REVISIÓN

### 2.1 Funcionalidad
- [ ] El código cumple con el spec.md (User Stories)
- [ ] Todos los criterios de aceptación están implementados
- [ ] No hay funcionalidades "de regalo" (scope creep)
- [ ] Los errores se manejan gracefulmente (no crashan el servidor)

### 2.2 Tests
- [ ] Hay tests unitarios para funciones críticas
- [ ] Hay tests de integración para endpoints
- [ ] Todos los tests pasan (`pytest -v`, `npm test`)
- [ ] Cobertura > 80% (verificar con `pytest --cov`)
- [ ] Hay tests de edge cases (null, empty, too long, SQL injection)

### 2.3 Seguridad
- [ ] No hay secrets hardcodeados (buscar `password`, `key`, `token` en código)
- [ ] SQL Injection protegido (ORM usado, no concatenación de strings)
- [ ] XSS protegido (React escapa, o sanitización en backend)
- [ ] Rate limiting en APIs públicas
- [ ] Validación de inputs (Pydantic / Zod / Joi)
- [ ] Headers de seguridad (HSTS, CSP, X-Frame-Options)
- [ ] Dependencias auditadas (`npm audit`, `pip-audit`)

### 2.4 Calidad de Código
- [ ] Nombres descriptivos (funciones, variables, clases)
- [ ] Funciones cortas (< 50 líneas ideal, < 100 máximo)
- [ ] No hay código duplicado (DRY)
- [ ] Comentarios solo donde la lógica es compleja (no obvios)
- [ ] Linter pasa sin errores (`ruff check`, `eslint`)
- [ ] Formato consistente (`black`, `prettier`)

### 2.5 Documentación
- [ ] OpenAPI actualizado (si hay nuevos endpoints)
- [ ] README actualizado (si hay cambios de setup)
- [ ] ADR creado (si hay decisión arquitectura nueva)
- [ ] Comentarios de docstring en funciones públicas

### 2.6 Performance
- [ ] No hay N+1 queries (usar eager loading)
- [ ] Índices de BD justificados
- [ ] No hay carga de archivos grandes en memoria
- [ ] Cache usado donde aplica (Redis)

### 2.7 Git
- [ ] Commits siguen Conventional Commits
- [ ] Rama feature/XXX bien nombrada
- [ ] No hay commits de "WIP" o "temp"
- [ ] Rebase sobre main si hay conflictos

---

## 3. NIVELES DE APROBACIÓN

| Nivel | Quién | Cuándo |
|-------|-------|--------|
| **Aprobado** | ZEUS + Jelkin | Todo pasa, merge permitido |
| **Cambios solicitados** | ZEUS | ODIN debe corregir y re-push |
| **Rechazado** | ZEUS o Jelkin | No cumple spec, se cierra PR |
| **Auto-approve** | GitHub Actions | Solo lint + tests (no reemplaza review humano) |

---

## 4. ETIQUETA DE REVISIÓN

ZEUS debe usar estas etiquetas en los comentarios de PR:

| Etiqueta | Significado | Acción ODIN |
|----------|-------------|-------------|
| `[CRITICAL]` | Bug de seguridad o funcionalidad | Corregir antes de merge |
| `[MAJOR]` | Cambio importante, no bloqueante | Corregir o justificar |
| `[MINOR]` | Estilo, naming, preferencia | Corregir si aplica |
| `[NIT]` | Nitpick, opcional | ODIN decide |
| `[QUESTION]` | Duda de ZEUS | Responder con explicación |
| `[PM2]` | Falta artefacto PM2 | ZEUS lo genera, no bloquea código |

---

> "Un PR sin review es código que no existe."
> **ZEUS — Code Review Authority**
