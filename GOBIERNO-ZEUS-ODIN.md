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

## 1.1 Arquitectura de Documentos (Mapa Completo)

Para que Kimi (ODIN) sepa dónde está todo, aquí está el mapa completo:

```
Desarrollos/ (Repo de Código — ODIN trabaja aquí)
├── GOBIERNO-ZEUS-ODIN.md          ← ESTE DOCUMENTO: Reglas de gobierno
├── metodologia/
│   ├── AGENTS.md                  ← Identidad y límites de ODIN
│   ├── INICIO-SESION-ODIN.md     ← Checklist obligatorio al iniciar sesión
│   ├── SELECTOR.md               ← Decidir qué metodología aplica
│   ├── SELECTOR-METODOLOGIA.md    ← Proyectos físicos existentes
│   ├── ODIN-TRAD.md              ← Metodología desarrollo tradicional
│   ├── ODIN-IA.md                ← Metodología desarrollo IA
│   ├── SDD-INNOVADATACO.md        ← Fase ZERO: especificación antes de código
│   ├── standards/
│   │   ├── code-review.md        ← Checklist de revisión ZEUS
│   │   ├── commit-convention.md   ← Convención de commits
│   │   └── security-checklist.md ← Checklist de seguridad
│   └── templates/
│       ├── spec-template.md      ← Template de especificación
│       ├── plan-template.md       ← Template de plan técnico
│       ├── tasks-template.md      ← Template de tareas (DoD 12 items)
│       └── ADR-template.md        ← Template de decisiones arquitectura
└── PROYECTO-XXX/
    ├── specs/
    │   └── NNN-nombre/
    │       ├── spec.md            ← Especificación del módulo
    │       ├── plan.md            ← Plan técnico
    │       └── tasks.md           ← Tareas desglosadas
    ├── docs/
    │   └── auditoria/
    │       ├── ACTA-VALIDACION-XXX.md   ← Comprobante de validación
    │       ├── ACTA-CORRECCION-XXX.md    ← Acciones correctivas
    │       ├── DEUDAS-TECNICAS-XXX.md    ← Deuda técnica identificada
    │       └── INSTRUCCIONES-ODIN-XXX.md  ← Instrucciones para ODIN
    └── src/                        ← Código fuente (solo ODIN)

IDC_PROYECTOS/ (Repo de Gestión — ZEUS trabaja aquí)
├── SINCRONIZACION-MAESTRA.md      ← Estado global de todos los proyectos
├── INSTRUCCIONES/
│   └── INSTRUCCION-TEMPLATE.md   ← Template de instrucción formal
├── PORTFOLIO.md                  ← Visión ejecutiva de todos los proyectos
└── PROYECTO-XXX/
    └── 03-EJECUCION/
        ├── 01-REGISTROS-AVANCE.md  ← Registro de avances
        ├── 04-INCIDENCIAS.md       ← Incidencias detectadas
        └── 05-DECISIONES.md        ← Decisiones tomadas
```

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
| Leer de IDC_PROYECTOS (para referencia) | **Escribir, modificar, crear o eliminar en IDC_PROYECTOS** (solo ZEUS) |

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

---

## 5. SINCRONIZACIÓN Y COMUNICACIÓN ENTRE ZEUS Y ODIN

### 5.1 ¿Cómo se comunican ZEUS y ODIN?

**NO por chat.** ZEUS y ODIN no se escriben mensajes. Se comunican por:

1. **GitHub Issues** — Para tareas, bugs, gaps, solicitudes
2. **GitHub PRs** — Para revisión de código
3. **Documentos en repo** — Para actas, instrucciones, estados
4. **GitHub Actions** — Para CI/CD, tests automáticos

### 5.2 Ciclo de Sincronización

```
┌─────────────────────────────────────────────────────────────────┐
│  CICLO DE SINCRONIZACIÓN ZEUS ↔ ODIN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. JELKIN + ZEUS definen alcance (chat o reunión)              │
│     ↓                                                           │
│  2. ZEUS genera spec + plan + tasks en Desarrollos              │
│     ↓                                                           │
│  3. JELKIN revisa y firma INSTRUCCION-XXX.md                    │
│     ↓                                                           │
│  4. ZEUS sube INSTRUCCION-XXX.md a IDC_PROYECTOS                │
│     ↓                                                           │
│  5. ODIN lee AGENTS.md → SELECTOR → ODIN-TRAD → INSTRUCCION    │
│     ↓                                                           │
│  6. ODIN ejecuta (SETUP → IMPLEMENT)                            │
│     ↓                                                           │
│  7. ODIN commitea → GitHub Actions corre CI                     │
│     ↓                                                           │
│  8. ODIN crea PR → solicita validación de ZEUS                  │
│     ↓                                                           │
│  9. ZEUS valida (ACTA-VALIDACION o ACTA-CORRECCION)             │
│     ↓                                                           │
│  10. ZEUS actualiza SINCRONIZACION-MAESTRA.md                  │
│     ↓                                                           │
│  11. JELKIN revisa maestra → aprueba o pide ajustes            │
│     ↓                                                           │
│  12. Módulo N validado → JELKIN firma INSTRUCCION-(N+1)         │
│     ↓                                                           │
│  13. ODIN empieza Módulo N+1                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Documentos de Sincronización

| Documento | Quién lo escribe | Quién lo lee | Dónde está | Cuándo se actualiza |
|-----------|-----------------|--------------|------------|---------------------|
| SINCRONIZACION-MAESTRA.md | ZEUS | Jelkin + ODIN | IDC_PROYECTOS/ | 2x al día o cuando cambia estado |
| INSTRUCCION-XXX.md | ZEUS (genera) + Jelkin (firma) | ODIN | IDC_PROYECTOS/INSTRUCCIONES/ | Cuando Jelkin aprueba módulo nuevo |
| ACTA-VALIDACION-XXX.md | ZEUS | Jelkin + ODIN | Desarrollos/PROYECTO-XXX/docs/auditoria/ | Cuando ZEUS valida módulo |
| ACTA-CORRECCION-XXX.md | ZEUS | Jelkin + ODIN | Desarrollos/PROYECTO-XXX/docs/auditoria/ | Cuando ZEUS rechaza módulo |
| DEUDAS-TECNICAS-XXX.md | ZEUS | Jelkin + ODIN | Desarrollos/PROYECTO-XXX/docs/auditoria/ | Cuando ZEUS audita |

### 5.4 Reglas de Comunicación

**ZEUS hace:**
- Revisa PRs y genera actas
- Actualiza SINCRONIZACION-MAESTRA.md
- Crea instrucciones formales
- Pide correcciones a ODIN mediante ACTA-CORRECCION

**ODIN hace:**
- Lee INSTRUCCION-XXX.md antes de empezar
- Crea PRs y solicita revisión
- Reporta avance en INSTRUCCION-XXX.md (no en chat)
- Lee ACTA-CORRECCION y ejecuta correcciones
- NOTIFICA a ZEUS cuando termina correcciones (PR nuevo)

**Jelkin hace:**
- Firma instrucciones
- Aprueba/rechaza módulos
- Revisa SINCRONIZACION-MAESTRA.md periódicamente
- Interviene cuando ZEUS no revisa en 48h

### 5.5 Flujo de Instrucción Formal

```
Jelkin: "Zeus, necesito que ODIN corrija Módulo 001"
        ↓
ZEUS: Genera INSTRUCCION-ODIN-001.md
      - Alcance: Corregir bugs del Módulo 001
      - Fecha inicio: 2026-06-14
      - Fecha límite: 2026-06-16
      - Referencia: ACTA-CORRECCION-ODIN-001.md
      - Firma: Jelkin
        ↓
ZEUS: Sube INSTRUCCION-ODIN-001.md a IDC_PROYECTOS/INSTRUCCIONES/
        ↓
ODIN: Lee INSTRUCCION-ODIN-001.md al inicio de sesión
       ↓
ODIN: Ejecuta correcciones
       ↓
ODIN: Crea PR → "Módulo 001 corregido según ACTA-CORRECCION-ODIN-001"
       ↓
ZEUS: Revisa PR → Genera ACTA-VALIDACION-ODIN-001.md (si aprueba)
       ↓
ZEUS: Actualiza SINCRONIZACION-MAESTRA.md: Módulo 001 = VALIDADO
       ↓
Jelkin: Revisa maestra → aprueba o pide ajustes
```

### 5.6 Qué NO hacer NUNCA

| ❌ NO hacer | ✅ Hacer en su lugar |
|-------------|---------------------|
| ODIN pide instrucción por chat | ODIN lee INSTRUCCIONES/ en repo |
| ZEUS pide correcciones por chat | ZEUS genera ACTA-CORRECCION-XXX.md |
| Jelkin aprueba módulo por chat | Jelkin firma INSTRUCCION-XXX.md |
| ODIN declara "completado" por chat | ODIN declara "listo para validación" en PR |
| ZEUS pregunta "¿está listo?" por chat | ZEUS revisa PR y genera acta |

---

## 6. DEFINITION OF DONE (DoD) — CHECKLIST OBLIGATORIO

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
