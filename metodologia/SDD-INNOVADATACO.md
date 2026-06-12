# SDD-INNOVADATACO
## Software Development Definition — Innovadataco
**Versión:** 1.0.0  
**Propósito:** Definir el proceso de especificación antes de desarrollo (SDD)  
**Agente:** ODIN + ZEUS  
**Puente:** GitHub Issues + PRs  
**Regla:** Sin SDD completo, no hay `git checkout -b feature/XXX`.

---

## 1. ¿QUÉ ES SDD?

**SDD (Software Development Definition)** es la fase ZERO de cualquier proyecto/módulo en Innovadataco. Antes de escribir una línea de código, se debe definir:

- **Qué** se va a construir (spec.md)
- **Cómo** se va a construir (plan.md)
- **Con qué** se va a construir (stack, ADR)
- **Quién** lo valida (Jelkin)
- **Cuándo** se entrega (cronograma PM2 — ZEUS)

**Regla de oro:** Sin SDD completo y aprobado, no hay código.

---

## 2. FASES DEL SDD

### FASE 0: DETECCIÓN DE GAPS (ZEUS)
**Input:** Documentos del cliente (Word, PDF, Excel, reuniones)  
**Output:** `PROYECTO-XXX/docs/gaps.md` — Lista de información faltante  
**Tiempo:** 1-2 días  
**Responsable:** ZEUS (con soporte de Jelkin)

ZEUS lee todos los documentos del cliente y detecta:
- Requisitos ambiguos
- Datos faltantes (usuarios, volúmenes, integraciones)
- Riesgos técnicos
- Dependencias externas

**Si hay gaps críticos:** ZEUS crea GitHub Issue → Jelkin responde → Se cierra el gap antes de continuar.

### FASE 1: ESPECIFICACIÓN (ODIN + ZEUS)
**Input:** Documentos cliente + gaps cerrados  
**Output:** `PROYECTO-XXX/specs/NNN-nombre/spec.md`  
**Template:** `metodologia/templates/spec-template.md`  
**Tiempo:** 2-3 días  
**Responsable:** ODIN (redacta), ZEUS (revisa contra PM2), Jelkin (aprueba)

Contenido del spec.md:
- Resumen ejecutivo
- Alcance y fuera de alcance
- User Stories (formato: Como [rol], quiero [objetivo], para [beneficio])
- Requisitos funcionales (RF-001, RF-002...)
- Requisitos no funcionales (RNF-001: seguridad, performance, etc.)
- Reglas de negocio
- Mockups / Wireframes (links o descripciones)
- Criterios de aceptación (Gherkin: Given/When/Then)

### FASE 2: PLAN TÉCNICO (ODIN)
**Input:** spec.md aprobado  
**Output:** `PROYECTO-XXX/specs/NNN-nombre/plan.md` + `PROYECTO-XXX/specs/NNN-nombre/ADR-001.md`  
**Template:** `metodologia/templates/plan-template.md`  
**Tiempo:** 1-2 días  
**Responsable:** ODIN

Contenido del plan.md:
- Stack tecnológico (justificado)
- Arquitectura de alto nivel (diagrama textual o link)
- Modelo de datos (entidades, relaciones)
- API endpoints (métodos, rutas, request/response)
- Plan de seguridad (autenticación, autorización, encriptación)
- Estrategia de testing (unitario, integración, E2E)
- Estrategia de deploy (Docker, VPS, cloud)
- Estimación de esfuerzo (horas/personas)

### FASE 3: DESGLOSE DE TAREAS (ODIN)
**Input:** plan.md aprobado  
**Output:** `PROYECTO-XXX/specs/NNN-nombre/tasks.md`  
**Template:** `metodologia/templates/tasks-template.md`  
**Tiempo:** 1 día  
**Responsable:** ODIN

Contenido del tasks.md:
- Lista de tareas con IDs (TASK-001, TASK-002...)
- Cada tarea: descripción, criterios de aceptación, estimación, dependencias
- Asignación: ODIN ejecuta, ZEUS supervisa PM2
- Definición de Done (DoD): código + tests + docs + PR mergeado

### FASE 4: APROBACIÓN (JELKIN)
**Input:** spec.md + plan.md + tasks.md  
**Output:** GitHub Issue cerrado con label `approved`  
**Tiempo:** 1 día  
**Responsable:** Jelkin (aprueba), ZEUS (verifica PM2)

Jelkin revisa:
- ¿El spec cubre lo que el cliente pidió?
- ¿El plan es técnicamente viable?
- ¿Las estimaciones son realistas?
- ¿Falta algún artefacto PM2?

**Si Jelkin aprueba:** Se crea milestone en GitHub, se asignan tareas, ODIN inicia desarrollo.  
**Si Jelkin rechaza:** Se documentan correcciones, se itera FASE 1-3.

---

## 3. ESTRUCTURA DE CARPETAS SDD

```
PROYECTO-XXX-NOMBRE/
├── specs/
│   └── NNN-nombre-modulo/
│       ├── spec.md          ← Especificación funcional
│       ├── plan.md          ← Plan técnico
│       ├── tasks.md         ← Desglose de tareas
│       ├── ADR-001.md       ← Decisiones arquitectura
│       ├── ADR-002.md       ← Más ADRs si aplica
│       └── assets/          ← Mockups, diagramas, docs cliente
│           ├── wireframe-001.png
│           ├── diagrama-er.png
│           └── doc-cliente-v1.pdf
├── docs/
│   ├── cliente/             ← Documentos originales del cliente
│   ├── pm2/                 ← ← ← SOLO ZEUS TOCA ESTO
│   └── api/                 ← OpenAPI auto-generado
├── src/
│   ├── backend/
│   ├── frontend/
│   └── tests/
└── README.md
```

---

## 4. CHECKLIST DE APROBACIÓN SDD

Antes de que Jelkin apruebe, ZEUS debe verificar:

- [ ] spec.md tiene al menos 5 User Stories
- [ ] Cada User Story tiene criterios de aceptación (Given/When/Then)
- [ ] plan.md tiene stack justificado
- [ ] plan.md tiene modelo de datos
- [ ] plan.md tiene estrategia de seguridad (OWASP)
- [ ] tasks.md tiene todas las tareas desglosadas hasta < 8 horas cada una
- [ ] ADR-001.md existe si hay decisión arquitectura no trivial
- [ ] No hay [PENDIENTE] críticos sin respuesta de Jelkin
- [ ] Los 35 artefactos PM2 relevantes están referenciados
- [ ] Documentos del cliente están en `docs/cliente/`

---

## 5. INTEGRACIÓN CON PM2 (ZEUS)

Cada fase SDD genera o actualiza artefactos PM2:

| Fase SDD | Artefactos PM2 generados | Responsable |
|----------|-------------------------|-------------|
| FASE 0 (Gaps) | OPM2-02 (Acta), OPM2-03 (Stakeholders) | ZEUS |
| FASE 1 (Spec) | OPM2-04 (Plan), OPM2-05 (Alcance), OPM2-06 (Reqs) | ZEUS |
| FASE 2 (Plan) | OPM2-07 (Cronograma), OPM2-08 (Costos), OPM2-09 (Calidad) | ZEUS |
| FASE 3 (Tasks) | OPM2-10 (Recursos), OPM2-11 (Comms), OPM2-12 (Riesgos) | ZEUS |
| FASE 4 (Aprob) | OPM2-14 (Stakeholders actualizado) | ZEUS |

**ODIN no genera artefactos PM2. ODIN genera specs técnicos. ZEUS genera PM2.**

---

> "Un buen SDD es el 50% del proyecto. Un mal SDD es el 200% (retrabajo)."
> **SDD — Innovadataco**
