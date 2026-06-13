# TASKS-001: Desglose de Tareas — Registro Anónimo de Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-12  
**Autor:** ODIN (CEO IA Dev)  
**Metodología:** ODIN-TRAD + ODIN-IA

---

## 1. DEFINICIÓN DE DONE (DoD)

Una tarea está "Done" cuando:
- [x] Código implementado y commiteado
- [x] Tests unitarios pasan (pytest / vitest)
- [x] Tests de integración pasan (TestClient / Testing Library)
- [x] Linter pasa sin errores (ruff / black / eslint)
- [x] Documentación actualizada (README / SDD / ADR)
- [ ] Code review aprobado por ZEUS
- [x] PR mergeado a `setup/estructura-2026`
- [ ] Artefactos PM2 actualizados (ZEUS)

---

## 2. DESGLOSE DE TAREAS

### FASE 1: SEGURIDAD CRÍTICA

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-001 | Eliminar secret hardcodeado | `config.py` solo lee `REPORT_ENCRYPTION_KEY` de env var | Arranque falla si falta o es inválida | 2h | Ninguna | ODIN |
| TASK-002 | Headers de seguridad OWASP | Middleware con HSTS, CSP, X-Frame, etc. | Tests verifican headers en respuestas | 3h | Ninguna | ODIN |
| TASK-003 | Restringir CORS | `allow_methods` y `allow_headers` acotados | CORS no permite origen desconocido | 1h | Ninguna | ODIN |
| TASK-004 | Crear `.env.example` | Variables de entorno documentadas | Archivo presente sin valores reales | 1h | TASK-001 | ODIN |

### FASE 2: RATE LIMITING Y REDIS

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-010 | Redis fallback para rate limit | Usar Redis si `REDIS_URL` configurado; memoria si no | Warning en prod si usa memoria | 4h | Ninguna | ODIN |
| TASK-011 | Corregir dependencias | Eliminar `httpx2`, versionar `slowapi/redis/limits` | `pip install` exitoso | 1h | Ninguna | ODIN |

### FASE 3: BACKEND

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-020 | Endpoint POST /api/reportes | Crear reporte anónimo con validación | Tests pasan, retorna 201 + hash | 4h | TASK-001 | ODIN |
| TASK-021 | Modelo Report en SQLAlchemy | UUID, hash único, campos encriptados | Sin columnas de metadata prohibidas | 3h | TASK-020 | ODIN |
| TASK-022 | Servicio de encriptación | AES-256-GCM con DEK por campo | Roundtrip y tampering tests pasan | 4h | TASK-021 | ODIN |

### FASE 4: FRONTEND

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-030 | Formulario ReportForm | Campos requeridos, evidencia opcional | Renderiza y valida | 3h | TASK-020 | ODIN |
| TASK-031 | Manejo de errores | Mensajes claros para 422, 429, errores de red | Tests de vitest pasan | 2h | TASK-030 | ODIN |
| TASK-032 | Accesibilidad básica | Labels con `htmlFor` e inputs con `id` | Testing Library encuentra controles | 1h | TASK-030 | ODIN |

### FASE 5: TESTS Y COBERTURA

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-040 | Tests backend | pytest con cobertura | ≥ 80% cobertura, todos pasan | 4h | TASK-022, TASK-010 | ODIN |
| TASK-041 | Tests frontend | vitest para ReportForm | 5 tests pasan | 2h | TASK-031 | ODIN |

### FASE 6: DOCUMENTACIÓN SDD

| ID | Tarea | Descripción | Criterios de aceptación | Estimación | Dependencias | Asignado |
|----|-------|-------------|------------------------|------------|--------------|----------|
| TASK-050 | gaps.md | Gaps identificados y cierre | Archivo en `docs/gaps.md` | 1h | Ninguna | ODIN |
| TASK-051 | spec.md | Especificación funcional | Archivo en `specs/001-registro-anonimo/spec.md` | 2h | TASK-050 | ODIN |
| TASK-052 | plan.md | Plan técnico | Archivo en `specs/001-registro-anonimo/plan.md` | 2h | TASK-051 | ODIN |
| TASK-053 | tasks.md | Desglose de tareas | Archivo en `specs/001-registro-anonimo/tasks.md` | 1h | TASK-052 | ODIN |
| TASK-054 | ADR-001 | Decisión de seguridad y anonimato | Archivo en `specs/001-registro-anonimo/ADR-001-seguridad.md` | 1h | TASK-052 | ODIN |
| TASK-055 | README.md | Guía de uso y decisiones | Archivo en raíz del proyecto | 1h | TASK-051 | ODIN |

---

## 3. CRONOGRAMA (Gantt simplificado)

```
Día 1: [SEGURIDAD][========]
Día 2: [BACKEND][========]
Día 3: [FRONTEND][======]
Día 4: [TESTS][======]
Día 5: [DOCS SDD][======]
```

---

## 4. RIESGOS Y MITIGACIÓN

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Responsable |
|----|--------|-------------|---------|------------|-------------|
| R-001 | Clave de encriptación comprometida | Baja | Alto | Rotación manual y re-encriptación | ODIN + ZEUS |
| R-002 | Rate limit en memoria no escala | Media | Medio | Configurar Redis en prod | ODIN |
| R-003 | Abuso del formulario anónimo | Media | Medio | Rate limiting + monitoreo | ODIN + ZEUS |

---

## 5. DEPENDENCIAS EXTERNAS

| ID | Dependencia | Tipo | Estado | Bloquea |
|----|-------------|------|--------|---------|
| DEP-001 | Definición de proveedor de deploy | Externa | [PENDIENTE] | TASK-060 |
| DEP-002 | Requisitos legales para reportes de menores | Externa | [PENDIENTE] | Módulo 002 |

---

> Generado por ODIN — Innovadataco
