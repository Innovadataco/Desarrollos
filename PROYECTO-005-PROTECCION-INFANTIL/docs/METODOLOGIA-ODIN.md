# METODOLOGIA-ODIN.md

**Proyecto:** PROYECTO-005 — Protección Infantil (Semáforo de Confianza)  
**Autor:** ZEUS / ODIN  
**Fecha:** 14 de junio de 2026  
**Versión:** 1.0.0  

---

## 1. Propósito

Este documento define el proceso de desarrollo que ODIN debe seguir en el proyecto **Semáforo de Confianza**. Su objetivo es garantizar que el código, la documentación y los estados reportados sean verificables, auditables y validados por ZEUS antes de declarar cualquier módulo como "completado".

---

## 2. Principios de gobierno

1. **La verdad está en el repo.** Si no está commiteado y testeado, no existe.
2. **ODIN no declara "completado".** Solo puede declarar **"listo para validación"**.
3. **ZEUS valida estados.** Ningún módulo avanza sin Acta de Validación firmada.
4. **Jelkin aprueba.** Las instrucciones formales requieren su firma antes de iniciar un módulo nuevo.
5. **Anonimato y seguridad primero.** Cada cambio debe evaluar su impacto en la privacidad del reportante y del menor.

---

## 3. Proceso de desarrollo

### 3.1 Inicio de sesión

Al iniciar cada sesión, ODIN ejecuta el checklist de `metodologia/INICIO-SESION-ODIN.md`:

1. Sincronizar repositorio (`git pull origin setup/estructura-2026`).
2. Leer documentos de gobierno: `AGENTS.md`, `ODIN-TRAD.md`, `GOBIERNO-ZEUS-ODIN.md`.
3. Verificar proyectos físicos y estado en `SINCRONIZACION-MAESTRA.md`.
4. Confirmar instrucción formal vigente (`INSTRUCCIONES-ODIN-XXX.md`).

### 3.2 Durante el desarrollo

1. **Un cambio lógico por commit.** Cada commit debe ser atómico y referenciar el acta o instrucción correspondiente.
2. **Mensajes de commit:**
   - Formato: `tipo(alcance): descripción corta`
   - Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
   - Cuerpo: incluir `Refs: ACTA-XXX.md` o `Refs: INSTRUCCION-XXX.md` cuando aplique.
3. **Tests obligatorios:**
   - Backend: `pytest -q` (cobertura ≥ 80%).
   - Frontend: `npm test -- --run`.
   - E2E: `npx playwright test` cuando aplique.
4. **Linter obligatorio:**
   - Backend: `ruff check .`
   - Frontend: `npm run lint`
5. **No secrets en el código.** Claves, tokens y certificados solo por variables de entorno.

### 3.3 Cierre de tarea

Antes de declarar "listo para validación":

- [ ] Código implementado y funcional.
- [ ] Tests unitarios pasan.
- [ ] Tests de integración pasan.
- [ ] Cobertura ≥ 80%.
- [ ] Linter pasa sin errores.
- [ ] Documentación técnica actualizada.
- [ ] No hay secrets hardcodeados.
- [ ] Security checklist pasa.
- [ ] Commit referencia el acta/instrucción correspondiente.

---

## 4. Definition of Done (DoD)

Una funcionalidad se considera lista para validación cuando:

1. Cumple el criterio de aceptación del SPEC correspondiente.
2. Tiene tests automáticos que la verifican.
3. No introduce deuda técnica documentada sin plan de mitigación.
4. La documentación (spec, plan, tasks, README) refleja el estado real.
5. ZEUS puede reproducir el comportamiento con los tests.

---

## 5. Proceso de validación

```
ODIN declara "Listo para validación"
            │
            ▼
     ZEUS revisa código vs. spec
            │
            ├── ¿Cumple DoD? → SÍ → Acta de Validación → VALIDADO
            │
            └── ¿Cumple DoD? → NO → Acta de Corrección
                                       │
                                       ▼
                                  ODIN corrige
                                       │
                                       ▼
                                  ZEUS re-revisa
                                       │
                                       ▼
                                  SÍ → VALIDADO
```

**Regla de oro:** Ningún módulo puede declararse "COMPLETADO" sin revisión y aprobación de ZEUS.

---

## 6. Documentación relacionada

| Documento | Ubicación | Propósito |
|-----------|-----------|-----------|
| Inicio de sesión | `metodologia/INICIO-SESION-ODIN.md` | Checklist diario obligatorio |
| Gobierno | `GOBIERNO-ZEUS-ODIN.md` | Roles, flujo y reglas de decisión |
| Agente | `metodologia/AGENTS.md` | Identidad y límites de ODIN |
| Mejoras de metodología | `docs/auditoria/MEJORA-METODOLOGIA.md` | Lecciones del proceso de validación |
| Lecciones Módulo 001 | `docs/LECCIONES-001.md` | Aprendizajes de la primera corrección |
| Bitácora Módulo 001 | `docs/BITACORA-001.md` | Registro diario de avances |
| Template de PR | `.github/pull_request_template.md` | Checklist de calidad pre-merge |

---

## 7. Estándares de código

### Backend (Python / FastAPI)

- Usar type hints.
- Nombres en español para dominio del negocio.
- Servicios en `app/services/`, routers en `app/routers/`.
- Modelos en `app/models.py`, schemas en `app/schemas.py`.
- Cualquier cambio en modelos requiere considerar una migración Alembic antes de producción.

### Frontend (React / Vite / Tailwind)

- Componentes funcionales con hooks.
- Mobile-first (viewport 320px+).
- Sin tracking: sin cookies, sin localStorage, sin fingerprint.
- Validaciones de formato en cliente y servidor.

---

> **"La metodología no es burocracia: es la forma de mantener la calidad cuando la complejidad crece."**
> **ZEUS — CEO PMO, Innovadataco** ⚡
