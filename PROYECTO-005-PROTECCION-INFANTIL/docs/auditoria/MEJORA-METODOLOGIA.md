# MEJORA DE METODOLOGÍA — Proceso de Validación + Definition of Done
**Proyecto:** Innovadataco — Fábrica de Software  
**Fecha:** 14 de junio de 2026  
**Autor:** ZEUS (Auditor de Calidad)  
**Motivo:** Auditoría del Módulo 001 de PROYECTO-005 reveló que ODIN declaró tareas como "completadas" sin cumplir con el spec ni la metodología.

---

## 🔴 PROBLEMA IDENTIFICADO

La metodología `ODIN-TRAD.md` define 6 fases: **SPECIFY → PLAN → SETUP → IMPLEMENT → VALIDATE → RELEASE**.

**ODIN ejecutó:** SPECIFY → PLAN → SETUP → IMPLEMENT → **(saltó VALIDATE)** → RELEASE

Resultado: El Módulo 001 fue declarado "COMPLETADO" al 65%, con:
- 12 de 27 tasks marcadas ✅ que NO están en código
- Bug de seguridad en rate limiting (5/min vs 5/hr)
- Modelo de datos incompleto
- Frontend básico que no cumple SPEC-001

---

## ✅ SOLUCIÓN: REFORZAR FASE 5 (VALIDATE)

### Cambio #1: Definition of Done (DoD) Obligatorio

Cada task en `tasks.md` debe tener un **DoD checklist** verificable. ODIN no puede marcar ✅ sin pasar TODOS los checks.

**Template de DoD por task:**

```markdown
### Task: TF-001.6 — Selector de categoría
**DoD:**
- [ ] Campo en modelo SQLAlchemy (`category`, String, nullable)
- [ ] Campo en schema Pydantic (`ReportCreate` con `category`)
- [ ] Validación en router (CAT-01 a CAT-06)
- [ ] Selector en frontend con 6 opciones visibles
- [ ] Test unitario: validación de categoría válida
- [ ] Test unitario: rechazo de categoría inválida
- [ ] Test E2E: flujo completo con categoría seleccionada
- [ ] Code review por ZEUS (o auto-review si ZEUS no disponible)
- [ ] Security checklist: no expone datos sensibles
- [ ] Linter pasa sin errores (`ruff check`, `eslint`)
- [ ] Commit sigue conventional commits
- [ ] PR creado con descripción clara
```

**Regla:** Si falta UN check, la task está ⬜ **NO completada**.

---

### Cambio #2: Acta de Validación Obligatoria

Antes de declarar un módulo "COMPLETADO", ZEUS debe generar:

**Documento:** `docs/auditoria/VALIDACION-XXX.md`

```markdown
# ACTA DE VALIDACIÓN — Módulo XXX
**Proyecto:** [Nombre]  
**Módulo:** [XXX]  
**Fecha:** [YYYY-MM-DD]  
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
- [ ] No hay dependencias fantasmas (auditoría de requirements)

## Hallazgos
[Listar gaps encontrados, o "Ninguno"]

## Decisión
- [ ] ✅ APROBADO — Módulo declarado COMPLETADO
- [ ] ❌ RECHAZADO — Gaps críticos encontrados, ver ACTA-CORRECCION-ODIN.md

**Firma ZEUS:** [Nombre] | **Fecha:** [YYYY-MM-DD]
```

**Regla:** Sin Acta de Validación firmada, **el módulo NO está completado.**

---

### Cambio #3: Proceso de Corrección Formal

Si ZEUS rechaza (encuentra gaps):

```
1. ZEUS genera ACTA-CORRECCION-ODIN.md
   → Hallazgos, severidad, acciones correctivas, timeline
2. ZEUS sube a repo: docs/auditoria/ACTA-CORRECCION-ODIN-XXX.md
3. ODIN lee acta y crea rama fix/correccion-XXX
4. ODIN corrige gaps uno por uno, marcando checks
5. ODIN crea PR → GitHub Actions corre tests
6. ZEUS re-revisa (nueva Acta de Validación)
7. Si pasa → merge, tag release, Acta firmada
8. Si no → volver al paso 1
```

---

### Cambio #4: Separación Estricta ODIN/ZEUS

| Rol | Puede hacer | NO puede hacer |
|-----|-------------|----------------|
| **ODIN** | Leer, crear, modificar código y tests dentro de `src/`. Crear specs, plans, tasks, ADRs. Commits en feature branches. Deploy a staging. | Tocar `docs/auditoria/` (artefactos de auditoría). Crear carpetas de proyecto nuevo. Declarar "COMPLETADO" sin Acta de Validación. Merge a `main` sin aprobación. |
| **ZEUS** | Crear carpetas de proyecto. Generar artefactos PM2. Revisar código vs. specs. Generar Actas de Validación y Corrección. Aprobar/rechazar módulos. | Tocar `src/` (código). Hacer commits de código. |

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN DE ESTA MEJORA

- [ ] Agregar sección "DoD" a `metodologia/templates/tasks-template.md`
- [ ] Agregar sección "Acta de Validación" a `metodologia/ODIN-TRAD.md` (Fase 5)
- [ ] Agregar sección "Proceso de Corrección" a `metodologia/ODIN-TRAD.md`
- [ ] Crear template `metodologia/templates/validacion-template.md`
- [ ] Crear template `metodologia/templates/correccion-template.md`
- [ ] Actualizar `AGENTS.md` con regla: "Sin Acta de Validación, no hay COMPLETADO"
- [ ] Subir Acta de Corrección del Módulo 001 a `docs/auditoria/`
- [ ] Subir Deudas Técnicas del Módulo 001 a `docs/auditoria/`
- [ ] Subir esta mejora de metodología a `metodologia/MEJORA-VALIDACION.md`

---

## 🎯 CONCLUSIÓN

> **La metodología es buena. El problema es que no se aplica.**

Con estos 4 cambios, evitamos que vuelva a pasar:
1. **DoD checklist** por task → ODIN no puede marcar ✅ sin verificar
2. **Acta de Validación** → ZEUS debe revisar y firmar antes de "COMPLETADO"
3. **Proceso de Corrección** → Mecanismo formal cuando hay gaps
4. **Separación estricta** → Límites claros de quién toca qué

**ZEUS online. La calidad está operando.** ⚡
