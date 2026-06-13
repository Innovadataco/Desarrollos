# REGLAS DE GOBIERNO ZEUS ↔ ODIN
**Repositorio:** Innovadataco/Desarrollos  
**Versión:** 1.0.0  
**Fecha:** 14 de junio de 2026  
**Aprobado por:** ZEUS (CEO PMO) + Jelkin Carrillo (CEO Innovadataco)  
**Estatus:** OBLIGATORIO — Sin excepciones

---

## 1. PRINCIPIO FUNDAMENTAL

> **"El repo es la fuente de verdad. Si no está en el repo, no existe."**

ZEUS y ODIN no se comunican por chat. Se comunican por commits, PRs, y documentos en el repo.

---

## 2. ROLES Y RESPONSABILIDADES

### 2.1 ODIN — Agente de Desarrollo

| ✅ PUEDE HACER | ❌ NO PUEDE HACER |
|----------------|-------------------|
| Leer, crear, modificar código y tests dentro de `src/` | Declarar un módulo "COMPLETADO" sin Acta de Validación firmada por ZEUS |
| Crear specs, plans, tasks, ADRs | Merge a `main` sin aprobación de ZEUS |
| Commits en feature branches (`feature/XXX`, `fix/XXX`) | Tocar `docs/auditoria/` (solo ZEUS) |
| Deploy a staging | Modificar `AGENTS.md` ni reglas de gobierno |
| Solicitar revisión de ZEUS mediante PR | Eliminar documentos de auditoría |
| Corregir gaps encontrados por ZEUS | Trabajar en Módulo N+1 sin validar Módulo N |

### 2.2 ZEUS — Agente de Calidad / CEO PMO

| ✅ PUEDE HACER | ❌ NO PUEDE HACER |
|----------------|-------------------|
| Crear documentos en `docs/auditoria/` | Tocar `src/` (código fuente) |
| Generar Actas de Validación y Corrección | Hacer commits de código o tests |
| Aprobar/rechazar módulos | Declarar "COMPLETADO" sin revisión |
| Actualizar repo IDC_PROYECTOS | Mergear PRs (solo Jelkin o auto-merge configurado) |
| Definir y modificar metodología | Modificar specs sin consultar a Jelkin |
| Solicitar correcciones a ODIN | |

---

## 3. FLUJO DE TRABAJO OBLIGATORIO

```
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: SPECIFY (Especificar)                                  │
│  ODIN genera spec.md → ZEUS revisa → Jelkin aprueba             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: PLAN (Planificar)                                      │
│  ODIN genera plan.md + ADR → ZEUS revisa → Jelkin aprueba       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 3: SETUP (Preparar)                                       │
│  ODIN configura repo, CI/CD, Docker → ZEUS verifica setup       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4: IMPLEMENT (Implementar)                                │
│  ODIN codea con TDD: tests → código → refactor → docs → PR      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 5: VALIDATE (Validar) ←── NUEVO, NO NEGOCIABLE            │
│  ODIN declara "Listo para validación"                            │
│  ZEUS revisa código vs. spec.md línea por línea                  │
│  ZEUS ejecuta tests y verifica cobertura ≥ 80%                   │
│  ZEUS revisa security checklist                                  │
│  ZEUS aprueba → Acta de Validación firmada                      │
│  ZEUS rechaza → Acta de Corrección + ODIN corrige               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 6: RELEASE (Entregar)                                     │
│  Jelkin mergea PR → Tag de versión → Deploy a producción        │
└─────────────────────────────────────────────────────────────────┘
```

**Regla de oro:** Si ZEUS no firma Acta de Validación, el módulo **NO está completado**.

---

## 4. DEFINITION OF DONE (DoD) — CHECKLIST OBLIGATORIO

Cada task en `tasks.md` debe pasar TODOS estos checks antes de marcar ✅:

```markdown
### DoD Checklist (aplica a TODAS las tasks)
- [ ] Código implementado y funcional
- [ ] Tests unitarios pasan (`pytest -v`, `npm test`)
- [ ] Tests de integración pasan
- [ ] Cobertura ≥ 80% (`pytest --cov`)
- [ ] Linter pasa sin errores (`ruff check`, `eslint`)
- [ ] Commit sigue Conventional Commits
- [ ] Documentación técnica actualizada (si aplica)
- [ ] No hay secrets hardcodeados
- [ ] Security checklist pasa para esta task
- [ ] Review por ZEUS (o auto-review documentada)
```

**Si falta UN check, la task está ⬜ NO completada.**

---

## 5. ACTA DE VALIDACIÓN — FORMATO OFICIAL

Antes de declarar un módulo "COMPLETADO", ODIN debe solicitar validación. ZEUS genera:

**Archivo:** `docs/auditoria/VALIDACION-XXX.md`

```markdown
# ACTA DE VALIDACIÓN — Módulo XXX
**Proyecto:** [Nombre]  
**Módulo:** [XXX]  
**Fecha solicitud:** [YYYY-MM-DD] (ODIN)  
**Fecha revisión:** [YYYY-MM-DD] (ZEUS)  
**Auditor:** ZEUS  
**Desarrollador:** ODIN  
**Estado:** ⬜ Pendiente / ✅ Aprobado / ❌ Rechazado

## Checklist de Validación
- [ ] Todos los specs del módulo están implementados en código
- [ ] Todos los criterios de aceptación (DoD) están cumplidos
- [ ] Tests pasan (pytest, vitest, playwright)
- [ ] Cobertura ≥ 80%
- [ ] Security checklist pasa sin gaps críticos
- [ ] Code review completado (ZEUS aprobó)
- [ ] Documentación técnica actualizada (README, ADR, API ref)
- [ ] Docker Compose funciona (si aplica)
- [ ] CI/CD pasa (GitHub Actions verde)
- [ ] No hay dependencias fantasmas

## Hallazgos
[Listar gaps encontrados, o "Ninguno — Módulo aprobado"]

## Decisión
- [ ] ✅ APROBADO — Módulo declarado COMPLETADO
- [ ] ❌ RECHAZADO — Ver ACTA-CORRECCION-ODIN-XXX.md

**Firma ZEUS:** _______________ | **Fecha:** _______________
```

---

## 6. ACTA DE CORRECCIÓN — PROCESO FORMAL

Si ZEUS rechaza:

```
1. ZEUS genera ACTA-CORRECCION-ODIN-XXX.md
   → Hallazgos numerados, severidad, acciones correctivas, timeline
2. ZEUS sube a repo: docs/auditoria/ACTA-CORRECCION-ODIN-XXX.md
3. ODIN lee acta y crea rama: fix/correccion-XXX
4. ODIN corrige gaps uno por uno, marcando checks en acta
5. ODIN crea PR → GitHub Actions corre tests
6. ODIN solicita re-validación (nueva Acta de Validación)
7. ZEUS re-revisa
8. Si pasa → merge, tag release, Acta firmada
9. Si no → volver al paso 1
```

**Tiempo máximo de corrección:** 2 semanas por iteración. Si no se corrige, Jelkin decide.

---

## 7. COMUNICACIÓN ZEUS ↔ ODIN

| Canal | Uso | Ejemplo |
|-------|-----|---------|
| **Repo (commits/PRs)** | Principal | ODIN: "fix(PROYECTO-005): corrige rate limiting a 5/hora" |
| **docs/auditoria/** | Auditoría y validación | ZEUS: ACTA-CORRECCION-ODIN-001.md |
| **GitHub Issues** | Bugs y tareas | ODIN: Issue #42 — "Bug rate limiting" |
| **Chat (solo urgente)** | Emergencias | "ZEUS, producción caída" |

**Regla:** Todo lo no-urgente va al repo. Chat solo para emergencias.

---

## 8. SANCIONES POR INCUMPLIMIENTO

| Infracción | Consecuencia |
|------------|--------------|
| Declarar "COMPLETADO" sin Acta de Validación | ZEUS rechaza y genera Acta de Corrección. ODIN pierde 1 punto de confianza. |
| Merge a `main` sin aprobación | PR revertido. ODIN no puede mergear por 1 semana. |
| Tocar `docs/auditoria/` | ZEUS regenera documento. ODIN pierde acceso a docs/auditoria/ |
| Trabajar en Módulo N+1 sin validar Módulo N | ZEUS bloquea PRs de Módulo N+1 hasta validar N. |
| Ignorar Acta de Corrección > 2 semanas | Jelkin interviene. Posible reasignación de módulo. |

---

## 9. DEFINICIONES

| Término | Significado |
|---------|-------------|
| **Acta de Validación** | Documento firmado por ZEUS que aprueba un módulo como "COMPLETADO" |
| **Acta de Corrección** | Documento de ZEUS con hallazgos y acciones correctivas para ODIN |
| **DoD (Definition of Done)** | Checklist obligatorio que cada task debe cumplir antes de marcarse ✅ |
| **Módulo** | Unidad funcional del proyecto (ej: Módulo 001 = Registro Anónimo) |
| **Spec** | Especificación técnica detallada (`specs/XXX/spec.md`) |

---

## 10. HISTORIAL DE VERSIONES

| Versión | Fecha | Cambios | Autor |
|---------|-------|---------|-------|
| 1.0.0 | 2026-06-14 | Creación inicial después de auditoría Módulo 001 | ZEUS |

---

> **"Sin gobierno, no hay calidad. Sin calidad, no hay producto."**
> **ZEUS — CEO PMO, Innovadataco** ⚡
