# CASOS DE USO — Arquitectura ORDENES/
**Versión:** 1.0.0
**Fecha:** 2026-06-15
**Autor:** ZEUS (CEO PMO)
**Proyecto:** PROYECTO-005-PROTECCION-INFANTIL (aplicable a todos los proyectos)

---

## 📋 ACTORES

| Actor | Rol | Repositorio | Acceso ORDENES/ |
|-------|-----|-------------|-----------------|
| **Jelkin** | CEO Humano | Aprobador final | Lectura |
| **ZEUS** | CEO IA PMO | IDC_PROYECTOS + ORDENES/ | Lectura y escritura (GOBIERNO, TAREAS, VALIDACION) |
| **ODIN** | CEO IA Dev | Desarrollos (código) | Lectura y escritura (PROGRESO) |

---

## 🎯 CASO 1: Inicio de proyecto (Módulo 001)

### Contexto
Proyecto nuevo. Ningún módulo ha iniciado.

### ¿Qué hace Jelkin?
1. Le dice a ZEUS: "Necesito que ODIN desarrolle el Módulo 1 del Proyecto X"
2. Firma instrucción formal (INSTRUCCION-ODIN-001.md)
3. Nada más. No interactúa con ODIN.

### ¿Qué hace ZEUS?
1. Crea carpeta `ORDENES/` dentro del proyecto
2. Escribe `GOBIERNO.md`: estado de módulos, Módulo 1 = ACTIVO, reglas
3. Escribe `TAREAS-001.md`: lista de tareas del Módulo 1
4. Escribe `PROGRESO-001.md`: plantilla vacía
5. Escribe `VALIDACION-001.md`: plantilla vacía
6. Sube todo a GitHub

### ¿Qué hace ODIN?
1. Jelkin le dice: "ODIN, trabaja en PROYECTO-X"
2. ODIN lee `ORDENES/GOBIERNO.md` → sabe que Módulo 1 es ACTIVO
3. ODIN lee `ORDENES/TAREAS-001.md` → sabe qué hacer
4. ODIN desarrolla
5. ODIN reporta en `ORDENES/PROGRESO-001.md`

### Archivos modificados
- ZEUS: `GOBIERNO.md`, `TAREAS-001.md`, `VALIDACION-001.md` (creación)
- ODIN: `PROGRESO-001.md` (escritura), `src/` (código)

---

## 🎯 CASO 2: ODIN trabaja en una tarea

### Contexto
Módulo 1 está en desarrollo. ODIN va a implementar `TA-001.1`.

### ¿Qué hace Jelkin?
- **Nada.** ODIN trabaja solo. Jelkin solo interviene si hay bloqueos o decisiones.

### ¿Qué hace ZEUS?
- **Nada.** ZEUS auditará después, no durante el desarrollo.

### ¿Qué hace ODIN?
1. Lee `TAREAS-001.md` → identifica `TA-001.1`
2. Lee `specs/001-registro-anonimo/spec.md` → entiende requerimiento técnico
3. Desarrolla código en `src/`
4. Corre tests
5. Commitea: `git commit -m "feat(001): implement TA-001.1 - modelo User"`
6. Actualiza `PROGRESO-001.md`:
   ```markdown
   - [x] TA-001.1 — Implementar modelo User
     - Archivo: src/backend/app/models.py
     - Tests: 5 passed, 0 failed
     - Commit: a1b2c3d
   ```

### Archivos modificados
- ODIN: `PROGRESO-001.md`, `src/`, `tests/`

---

## 🎯 CASO 3: ODIN termina una tarea y reporta

### Contexto
ODIN acaba de terminar `TA-001.1` y quiere seguir con `TA-001.2`.

### ¿Qué hace Jelkin?
- **Nada.** ODIN reporta solo en `PROGRESO-001.md`.

### ¿Qué hace ZEUS?
- **Nada aún.** ZEUS auditará cuando ODIN declare el módulo listo.

### ¿Qué hace ODIN?
1. Verifica que tests pasan
2. Verifica que código funciona
3. Escribe en `PROGRESO-001.md`:
   ```markdown
   ## Reporte ODIN — 2026-06-15 14:00

   ### Tareas completadas
   - [x] TA-001.1 — Implementar modelo User
   - [x] TA-001.2 — Implementar endpoint login

   ### Tareas pendientes
   - [ ] TA-001.3 — Implementar endpoint refresh

   ### Estado: EN PROGRESO
   ```
4. Sigue trabajando en `TA-001.3`

### Archivos modificados
- ODIN: `PROGRESO-001.md`

---

## 🎯 CASO 4: ODIN declara "LISTO PARA VALIDACION"

### Contexto
ODIN terminó todas las tareas del Módulo 1. Quiere que ZEUS audite.

### ¿Qué hace Jelkin?
- **Nada.** ZEUS se encarga de la auditoría.

### ¿Qué hace ODIN?
1. Verifica DoD (12 items):
   - Código implementado ✅
   - Tests pasan ✅
   - Linter limpio ✅
   - Documentación actualizada ✅
   - etc.
2. Escribe en `PROGRESO-001.md`:
   ```markdown
   ### Estado general del módulo
   🟡 LISTO PARA VALIDACION

   Todas las tareas completadas. Commit final: z9y8x7w.
   ```
3. Hace push a GitHub
4. **No dice "completado".** Dice "listo para validación".

### ¿Qué hace ZEUS?
1. Lee `PROGRESO-001.md` → ve "LISTO PARA VALIDACION"
2. Lee `TAREAS-001.md` → sabe qué debería estar implementado
3. Lee `specs/001-registro-anonimo/spec.md` → sabe requerimientos técnicos
4. Revisa código en `src/` línea por línea
5. Corre tests
6. Verifica commits
7. Escribe en `VALIDACION-001.md`:
   ```markdown
   ## Auditoría ZEUS — 2026-06-15 20:00

   | Tarea | Código | Tests | Spec | Resultado |
   |-------|--------|-------|------|-----------|
   | TA-001.1 | ✅ | ✅ | ✅ | ✅ APROBADO |
   | TA-001.2 | ✅ | ✅ | ✅ | ✅ APROBADO |
   | TA-001.3 | ✅ | ❌ | ✅ | ❌ RECHAZADO |

   ### Decisión
   ❌ MÓDULO RECHAZADO. TA-001.3: Tests fallan. Corregir y re-auditar.
   ```

### Archivos modificados
- ODIN: `PROGRESO-001.md` (estado actualizado)
- ZEUS: `VALIDACION-001.md` (auditoría)

---

## 🎯 CASO 5: ZEUS rechaza, ODIN corrige

### Contexto
ZEUS rechazó el Módulo 1. ODIN debe corregir `TA-001.3`.

### ¿Qué hace Jelkin?
- **Nada.** ZEUS ya dio instrucciones claras en `VALIDACION-001.md`.

### ¿Qué hace ODIN?
1. Lee `VALIDACION-001.md` → ve que `TA-001.3` fue rechazado
2. Lee hallazgo: "Tests fallan"
3. Corrige código
4. Corre tests hasta que pasen
5. Actualiza `PROGRESO-001.md`:
   ```markdown
   ### Correcciones post-auditoría
   - TA-001.3 — Corregido. Tests ahora pasan (5/5). Commit: b2c3d4e.
   ```
6. Declara nuevamente: "LISTO PARA VALIDACION"

### ¿Qué hace ZEUS?
1. Lee `PROGRESO-001.md` → ve correcciones
2. Re-audita `TA-001.3`
3. Escribe en `VALIDACION-001.md`:
   ```markdown
   ### Re-auditoría — 2026-06-16 10:00
   | Tarea | Resultado |
   |-------|-----------|
   | TA-001.3 | ✅ APROBADO |

   ### Decisión final
   ✅ MÓDULO 001 VALIDADO
   ```
4. Actualiza `GOBIERNO.md`:
   ```markdown
   | 001 | Registro Anónimo | ✅ VALIDADO | ZEUS | 2026-06-16 |
   | 002 | Consulta Semáforo | 🟢 ACTIVO | — | — |
   ```

### Archivos modificados
- ODIN: `PROGRESO-001.md`, `src/`, `tests/`
- ZEUS: `VALIDACION-001.md`, `GOBIERNO.md`

---

## 🎯 CASO 6: ODIN pierde contexto (cierra VS Code)

### Contexto
ODIN cerró VS Code. Abre Kimi nuevo. No sabe nada.

### ¿Qué hace Jelkin?
1. Abre Kimi
2. Pega las 2 líneas:
   ```
   ODIN, lee el archivo PROYECTO-005-PROTECCION-INFANTIL/ORDENES/GOBIERNO.md 
   y dime qué módulo está activo y qué tareas hay pendientes.
   ```
3. Espera respuesta

### ¿Qué hace ODIN?
1. Lee `GOBIERNO.md`
2. Responde: "Módulo activo: 005 — Panel Admin. Tareas pendientes: 26"
3. Jelkin dice: "Lee TAREAS-005.md y empieza a desarrollar."
4. ODIN lee `TAREAS-005.md`
5. ODIN lee `PROGRESO-005.md` → ve qué ya se hizo
6. ODIN continúa desde donde quedó

### ¿Qué hace ZEUS?
- **Nada.** Este caso es entre Jelkin y ODIN. ZEUS no interviene.

### Archivos modificados
- Ninguno. Solo lectura.

---

## 🎯 CASO 7: Jelkin quiere autorizar excepción (Módulo 5 sin validar 4)

### Contexto
Módulo 4 tiene deudas técnicas. Jelkin quiere que ODIN avance al 5.

### ¿Qué hace Jelkin?
1. Le dice a ZEUS: "Autorizo avanzar al Módulo 5 sin validar el 4. Las deudas las dejamos para después."
2. Firma instrucción excepción (INSTRUCCION-ODIN-004-EXCEPCION.md)

### ¿Qué hace ZEUS?
1. Actualiza `GOBIERNO.md`:
   ```markdown
   | 004 | Clustering | ⚠️ EXCEPCIÓN | 3 deudas técnicas diferidas a 2026-06-21 |
   | 005 | Panel Admin | 🟢 ACTIVO | Autorizado por CEO |
   ```
2. Escribe `TAREAS-005.md` con tareas del Módulo 5
3. Sube a GitHub

### ¿Qué hace ODIN?
1. Lee `GOBIERNO.md` → ve "005 ACTIVO"
2. Lee `TAREAS-005.md`
3. Empieza a desarrollar
4. Reporta en `PROGRESO-005.md`

### Archivos modificados
- ZEUS: `GOBIERNO.md`, `TAREAS-005.md`
- ODIN: `PROGRESO-005.md`, `src/`

---

## 🎯 CASO 8: ZEUS audita progreso parcial (sin que ODIN termine)

### Contexto
ZEUS quiere ver cómo va ODIN sin esperar a que termine el módulo.

### ¿Qué hace Jelkin?
- **Nada.** ZEUS audita cuando quiere.

### ¿Qué hace ZEUS?
1. Lee `PROGRESO-005.md` → ve qué dice ODIN
2. Revisa código en `src/` → verifica si coincide con lo reportado
3. Escribe en `VALIDACION-005.md` (auditoría parcial):
   ```markdown
   ## Auditoría parcial — 2026-06-15 18:00

   | Tarea | Estado ODIN | Verificación ZEUS | Resultado |
   |-------|-------------|-------------------|-----------|
   | TF-005.1 | Completado | Revisado código | ✅ Coincide |
   | TF-005.2 | En progreso | Revisado código | 🟡 60% listo, coincide con reporte |

   ### Nota
   No es auditoría final. Módulo aún en desarrollo.
   ```

### ¿Qué hace ODIN?
- **Nada.** ZEUS no bloquea el trabajo. Solo verifica.

### Archivos modificados
- ZEUS: `VALIDACION-005.md`

---

## 📊 RESUMEN DE RESPONSABILIDADES

| Tarea | Jelkin | ZEUS | ODIN |
|-------|--------|------|------|
| Crear ORDENES/ | — | ✅ | — |
| Escribir GOBIERNO.md | — | ✅ | — |
| Escribir TAREAS-XXX.md | — | ✅ | — |
| Escribir VALIDACION-XXX.md | — | ✅ | — |
| Escribir PROGRESO-XXX.md | — | — | ✅ |
| Desarrollar código | — | — | ✅ |
| Auditar módulo | — | ✅ | — |
| Firmar instrucciones | ✅ | — | — |
| Recuperar contexto de ODIN | ✅ (2 líneas) | — | ✅ (lee archivos) |
| Aprobar excepciones | ✅ | — | — |

---

## 🚀 FLUJO GENERAL

```
Jelkin firma instrucción → ZEUS crea ORDENES/ (GOBIERNO + TAREAS)
                                    ↓
                              ODIN lee archivos
                                    ↓
                              ODIN desarrolla + reporta en PROGRESO
                                    ↓
                              ZEUS audita (cuando quiere o cuando ODIN dice "listo")
                                    ↓
                              ZEUS escribe VALIDACION
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
              ✅ VALIDADO                        ❌ RECHAZADO
                    ↓                               ↓
              ZEUS actualiza                     ODIN corrige
              GOBIERNO.md →                      ↓
              siguiente módulo              ZEUS re-audita
```

---

> **"Cada actor tiene su archivo. Nadie pisa al otro."**
> **ZEUS — CEO PMO**
