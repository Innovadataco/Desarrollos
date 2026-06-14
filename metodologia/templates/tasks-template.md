# TASKS-{ID}: {NOMBRE DEL DESGLOSE DE TAREAS}
## Proyecto: {PROYECTO-ID} — {NOMBRE PROYECTO}
**Versión:** 1.0.0  
**Fecha:** {YYYY-MM-DD}  
**Autor:** ODIN (CEO IA Dev)  
**Metodología:** ODIN-TRAD / ODIN-IA / Ambas

---

## 1. DEFINICIÓN DE DONE (DoD) — 12 items

Una tarea está "Done" cuando:
- [ ] Código implementado y commiteado
- [ ] Tests unitarios pasan (pytest / vitest)
- [ ] Tests de integración pasan (TestClient / Playwright)
- [ ] Linter pasa sin errores (ruff / black / eslint)
- [ ] Documentación actualizada (OpenAPI / README / ADR)
- [ ] Code review aprobado por ZEUS
- [ ] PR mergeado a `main`
- [ ] Artefactos PM2 actualizados (ZEUS)
- [ ] Código vs spec.md validado (cada función del spec existe en código)
- [ ] Security checklist completado (0 críticos)
- [ ] Sin deuda técnica nueva
- [ ] Estado real vs declarado: ZEUS valida que el % real = % declarado

**Regla:** ZEUS es el único que puede marcar el item #12. ODIN marca los items 1-11 como "LISTO PARA REVISIÓN", ZEUS confirma.

---

## 2. DESGLOSE DE TAREAS

### FASE 1: SETUP (Infraestructura)

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-001 | {Nombre} | {Descripción} | {Criterios} | {X}h | Ninguna | ODIN |
| TASK-002 | {Nombre} | {Descripción} | {Criterios} | {X}h | TASK-001 | ODIN |

### FASE 2: BACKEND (API + Lógica)

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-010 | {Nombre} | {Descripción} | {Criterios} | {X}h | TASK-002 | ODIN |

### FASE 3: FRONTEND (UI + UX)

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-020 | {Nombre} | {Descripción} | {Criterios} | {X}h | TASK-010 | ODIN |

### FASE 4: TESTS (Validación)

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-030 | {Nombre} | {Descripción} | {Criterios} | {X}h | TASK-020 | ODIN |

### FASE 5: DOCUMENTACIÓN + DEPLOY

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-040 | {Nombre} | {Descripción} | {Criterios} | {X}h | TASK-030 | ODIN |

---

## 3. CRONOGRAMA (Gantt simplificado)

```
Semana 1: [SETUP][====]
Semana 2: [BACKEND][========]
Semana 3: [FRONTEND][========]
Semana 4: [TESTS][====]
Semana 5: [DOCS+DEPLOY][====]
```

---

## 4. RIESGOS Y MITIGACIÓN

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Responsable |
|----|--------|-------------|---------|------------|-------------|
| R-001 | {Descripción} | Alta/Media/Baja | Alto/Medio/Bajo | {Acción} | ODIN/ZEUS |

---

## 5. DEPENDENCIAS EXTERNAS

| ID | Dependencia | Tipo | Estado | Bloquea |
|----|-------------|------|--------|---------|
| DEP-001 | {API de terceros / Documento cliente / Aprobación} | Externa | [PENDIENTE] | TASK-XXX |

---

> Generado por ODIN — Innovadataco
