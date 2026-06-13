# ODIN-TRAD
## Metodología de Desarrollo de Software Tradicional - Innovadataco
**Basada en:** Scrum + XP + Trunk-Based Development + Twelve-Factor App
**Para:** Apps web, sistemas de información, ITS, APIs, productos digitales sin IA central
**Agente:** ODIN (Kimi Code CLI)
**Gobernanza:** ZEUS (PM2) + Jelkin (CEO)

---

## 1. FILOSOFÍA

**"Código que no está en producción con tests pasando, es código que no existe."**

- Ciclos cortos (1-2 semanas por sprint)
- Tests antes que código (TDD)
- Integración continua (cada feature va a main vía PR)
- Documentación viva (se genera con el código)
- Especificación antes que implementación (SDD)

---

## 2. CICLO DE VIDA (6 FASES)

### FASE 1: SPECIFY (Especificar) - 1-2 días
**Quién:** ZEUS genera, Jelkin aprueba
**Qué:** User Stories, criterios de aceptación, requisitos funcionales/no funcionales
**Output:** `specs/XXX/spec.md` + artefactos PM2 (OPM2-02, OPM2-03)

### FASE 2: PLAN (Planificar) - 1-2 días
**Quién:** ODIN propone, Jelkin aprueba
**Qué:** Stack técnico, arquitectura, modelo de datos, APIs, seguridad
**Output:** `specs/XXX/plan.md` + ADR-001

### FASE 3: SETUP (Preparar) - 1 día
**Quién:** ODIN ejecuta
**Qué:** Estructura de carpetas, Docker, CI/CD, linter, tests base
**Output:** Repo funcional, CI verde

### FASE 4: IMPLEMENT (Implementar) - 1-2 semanas
**Quién:** ODIN ejecuta, Jelkin supervisa
**Qué:** TDD por feature: tests → código → refactor → docs → PR
**Output:** Código + tests + docs + PR en GitHub

### FASE 5: VALIDATE (Validar) — 1-2 días
**Quién:** ZEUS revisa, Jelkin aprueba final
**Qué:** Revisión de PR contra spec.md + plan.md + tasks.md + código
**Input:** PR + spec.md + plan.md + tasks.md + código
**Output:** ACTA-VALIDACION-XXX.md o ACTA-CORRECCION-XXX.md

#### 5.1 Proceso de Validación ZEUS (Obligatorio)

1. **ZEUS ejecuta checklist de validación**
   - Usar `metodologia/standards/code-review.md` como checklist
   - Verificar cada item de DoD (12 items del tasks-template.md)
   - Todos los tests pasan (pytest + vitest + playwright)
   - Cobertura > 80%
   - Linter sin errores

2. **ZEUS compara código vs spec.md línea por línea**
   - Cada User Story del spec tiene implementación en código
   - Cada RF (Requisito Funcional) está cubierto
   - Cada RNF (Requisito No Funcional) cumple criterio
   - No hay scope creep (funcionalidades de regalo)

3. **ZEUS verifica DoD de cada task**
   - Código implementado y commiteado
   - Tests unitarios pasan
   - Tests de integración pasan
   - Linter pasa sin errores
   - Documentación actualizada (OpenAPI / README / ADR)
   - Code review aprobado por ZEUS (este paso)
   - PR mergeado a main (después de aprobación)
   - Artefactos PM2 actualizados (ZEUS)
   - Código vs spec.md validado (cada función del spec existe en código)
   - Security checklist completado (0 críticos)
   - Sin deuda técnica nueva
   - Estado real vs declarado: ZEUS valida que el % real = % declarado

4. **ZEUS genera documento formal**
   - Si aprueba: `ACTA-VALIDACION-XXX.md` en `docs/auditoria/`
   - Si rechaza: `ACTA-CORRECCION-XXX.md` en `docs/auditoria/`
   - Documento incluye: fecha, revisión ZEUS, hallazgos, decisión, acciones

5. **ZEUS tiene 48h para revisar un PR**
   - Si no revisa en 48h → Jelkin interviene
   - Si está ocupado → ZEUS notifica a Jelkin con `[PENDIENTE-REVISION]`

#### 5.2 Regla de Oro de VALIDATE

> **Sin ACTA-VALIDACION-XXX.md firmada por ZEUS, el módulo NO está completado.**
>
> - ODIN no puede mergear a main
> - ODIN no puede iniciar Módulo N+1
> - ODIN no puede declarar "completado"
> - Jelkin no puede aprobar release sin Acta de Validación

#### 5.3 Niveles de Aprobación

| Nivel | Quién | Cuándo | Resultado |
|-------|-------|--------|-----------|
| **Aprobado** | ZEUS + Jelkin | Todo pasa, Acta generada | Merge a main permitido |
| **Cambios solicitados** | ZEUS | Hallazgos menores | ODIN corrige y re-push |
| **Rechazado** | ZEUS o Jelkin | No cumple spec | Se cierra PR, nuevo ciclo |

#### 5.4 Etiquetas de Validación ZEUS

ZEUS debe usar estas etiquetas en PR y documentos:

| Etiqueta | Significado | Acción ODIN |
|----------|-------------|-------------|
| `[CRITICAL]` | Bug de seguridad o funcionalidad | Corregir antes de merge |
| `[MAJOR]` | Cambio importante, no bloqueante | Corregir o justificar |
| `[MINOR]` | Estilo, naming, preferencia | Corregir si aplica |
| `[NIT]` | Nitpick, opcional | ODIN decide |
| `[QUESTION]` | Duda de ZEUS | Responder con explicación |
| `[PM2]` | Falta artefacto PM2 | ZEUS lo genera, no bloquea código |
| `[VALIDATED]` | Módulo validado | Listo para merge |
| `[REJECTED]` | Módulo rechazado | Nuevo ciclo de implementación |

### FASE 6: RELEASE (Entregar) — 1-2 días
**Quién:** ODIN genera, Jelkin deploya
**Qué:** Docker prod, runbook, tag de versión
**Output:** Release vX.Y.Z + OPM2-19
**Condición:** Solo si FASE 5 (VALIDATE) generó ACTA-VALIDACION-XXX.md

---

## 3. STACK ESTÁNDAR

### Tipo A: Web/App/SaaS (Proyecto 005, futuros productos)
| Capa | Tecnología |
|------|-----------|
| Frontend | React 19 + Vite + Tailwind + PWA |
| Backend | FastAPI + SQLAlchemy + PostgreSQL |
| Tests | pytest + Vitest + Playwright |
| Auth | OAuth2 + JWT + bcrypt |
| DevOps | Docker + GitHub Actions |
| Docs | OpenAPI auto + Markdown |

### Tipo B: Sistema de Información / ITS (Proyecto 001, 004)
| Capa | Tecnología |
|------|-----------|
| Frontend | React + MapLibre (GIS) |
| Backend | FastAPI + GeoAlchemy |
| Base de datos | PostgreSQL + PostGIS |
| IoT | MQTT + Node-RED (prototipos) |

### Tipo C: MVP Rápido (Proyecto 003, validaciones)
| Capa | Tecnología |
|------|-----------|
| Frontend | Next.js + Tailwind |
| Backend | Next.js API + Prisma |
| Base de datos | PostgreSQL (Neon/Vercel) |

---

## 4. ESTRUCTURA DE CARPETAS (obligatoria)

```
/proyecto/
├── README.md
├── AGENTS.md
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── .github/workflows/ci.yml
├── specs/
│   └── 001-feature/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── src/
│   ├── frontend/
│   ├── backend/
│   ├── shared/
│   └── tests/
├── docs/
│   ├── api/ (OpenAPI)
│   ├── adr/ (Architecture Decision Records)
│   └── tecnicos/
└── scripts/ (deploy, backup)
```

---

## 5. ESTÁNDARES DE CÓDIGO

### Commits (Conventional Commits)
```
feat: agregar endpoint de registro anónimo
fix: corregir validación de número telefónico
docs: actualizar README con instrucciones de deploy
test: agregar tests de integración para scoring
refactor: simplificar lógica de encriptación
security: rotar secrets, validar OWASP
```

### Tests obligatorios
- Unitarios: cada función crítica (pytest, vitest)
- Integración: cada endpoint de API (TestClient)
- E2E: flujos completos de usuario (Playwright)
- Cobertura mínima: 80%

### Seguridad (OWASP Top 10)
- [ ] No secrets hardcodeados
- [ ] SQL Injection protegido (ORM)
- [ ] XSS protegido (React escapa automático)
- [ ] CSRF tokens en formularios
- [ ] Rate limiting en APIs
- [ ] Encriptación en reposo
- [ ] Headers de seguridad (HSTS, CSP)
- [ ] Dependencias auditadas (npm audit, pip-audit)

---

## 6. FLUJO DE TRABAJO CON ZEUS

```
Jelkin: "ODIN, desarrolla el módulo X"
  ↓
ODIN: Lee spec.md → Genera plan.md → Jelkin aprueba
  ↓
ODIN: Implementa (TDD) → Crea PR en GitHub
  ↓
ZEUS: Revisa PR vs spec.md y PM2 → "APROBADO" o "RECHAZADO"
  ↓
Jelkin: Mergea PR
  ↓
ZEUS: Actualiza artefactos PM2
```

---

> "Código limpio, tests verdes, docs claras. Nada más, nada menos."
> ODIN - Fábrica de Software Innovadataco
