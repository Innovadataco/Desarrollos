# INICIO DE SESIÓN — ODIN (Kimi Code CLI)
**Repositorio:** Innovadataco/Desarrollos  
**Versión:** 1.0.0  
**Fecha:** 14 de junio de 2026  
**Autor:** ZEUS (CEO PMO)  
**Propósito:** Checklist obligatorio que ODIN debe ejecutar al inicio de CADA sesión

---

## ⚠️ REGla DE ORO

> **Si no ejecutas este checklist, no sabes en qué estado está el proyecto. Si no sabes el estado, no puedes codear.**

**Tiempo estimado:** 2-3 minutos  
**Frecuencia:** Cada vez que inicies sesión en Kimi Code CLI

---

## CHECKLIST DE INICIO (Ejecutar en orden)

### PASO 0: Identidad
```
"Soy ODIN. CEO IA de la Fábrica de Software Innovadataco.
Autonomía: SÍ en código. NO en gobernanza.
ZEUS valida estados. Jelkin aprueba."
```

### PASO 1: Sincronizar Repositorio
```bash
cd /ruta/al/repo/Desarrollos
git pull origin setup/estructura-2026
```
- [ ] Repo actualizado. Si hay conflictos → NOTIFICAR a ZEUS, no resolver solo.

### PASO 2: Leer Documentos de Gobierno (en orden) — **CRÍTICO SI PERDISTE CONTEXTO**

**⚠️ Si cerraste VS Code, perdiste la sesión, o no recuerdas el estado: DEBES leer estos documentos ANTES de tocar código.**

Leer estos documentos SÍ o SÍ antes de tocar código:

1. [ ] **`metodologia/GOBIERNO-ZEUS-ODIN.md`** → **PRIMERO Y SIEMPRE.** Flujo de trabajo, 3 candados, quién valida, quién aprueba, qué repo toca cada quien
2. [ ] **`metodologia/AGENTS.md`** → Recordar quién soy, qué puedo hacer, qué NO puedo hacer
3. [ ] **`../SINCRONIZACION-MAESTRA.md`** (subir un directorio, repo IDC_PROYECTOS) → Estado REAL de todos los módulos
4. [ ] **`INSTRUCCION-ODIN-XXX.md`** → Instrucción formal vigente (si existe)
5. [ ] **`INICIO-SESION-ODIN.md`** (este archivo) → Confirmar que ejecuté checklist

**Nota sobre SELECTOR-METODOLOGIA.md y ODIN-TRAD.md:**
- `SELECTOR-METODOLOGIA.md`: Ya no es crítico. Solo lista proyectos. Lee si quieres contexto histórico.
- `ODIN-TRAD.md`: Ya no es la metodología activa. El documento de gobierno real está en `GOBIERNO-ZEUS-ODIN.md`.

### PASO 3: Verificar Proyectos Físicos
```bash
ls -d PROYECTO-*/
```
- [ ] Lista de carpetas físicas coincide con `SELECTOR-METODOLOGIA.md`
- [ ] Si hay proyecto en matriz pero NO en disco → DETENER. Notificar a ZEUS/Jelkin.
- [ ] Si hay proyecto en disco pero NO en matriz → NOTIFICAR a ZEUS.

### PASO 4: Verificar Estado Actual

Leer documentos de estado:

1. [ ] **`../SINCRONIZACION-MAESTRA.md`** (repo IDC_PROYECTOS, subir un directorio) → **ESTADO REAL de todos los módulos. ESTE ES EL DOCUMENTO MAESTRO.**
2. [ ] **`INSTRUCCION-ODIN-XXX.md`** (si existe) → Verificar instrucciones pendientes
3. [ ] **`PROYECTO-005-PROTECCION-INFANTIL/docs/auditoria/`** → Verificar actas de validación/corrección

**Estado actual de PROYECTO-005 (14 de junio 2026, 23:45 CST):**
```
Módulo 001: ✅ VALIDADO v2 (ACTA-VALIDACION-ODIN-001-v2.md)
Módulo 002: ✅ VALIDADO (ACTA-VALIDACION-ODIN-002.md)
Módulo 003: ✅ VALIDADO (ACTA-VALIDACION-ODIN-003.md)
Módulo 004: ⚠️ VALIDADO CON EXCEPCIÓN (3 deudas técnicas diferidas a 21 junio)
Módulo 005: 🟢 AUTORIZADO (INSTRUCCION-ODIN-004-EXCEPCION.md)
Módulo 006: 🟢 AUTORIZADO (INSTRUCCION-ODIN-004-EXCEPCION.md)
```

**⚠️ Si ves otro estado en estos documentos, NO está actualizado. Usa lo que dice SINCRONIZACION-MAESTRA.md.**

### PASO 5: Verificar Instrucción Formal Vigente

- [ ] ¿Existe `INSTRUCCION-XXX.md` firmada por Jelkin?
- [ ] ¿La instrucción es para el módulo que voy a trabajar?
- [ ] ¿La instrucción tiene fecha de inicio y fecha límite?

**Si NO hay instrucción formal:**
- No empezar módulo nuevo
- Preguntar a Jelkin: "¿Tienes instrucción formal para el siguiente módulo?"
- Esperar a que ZEUS suba `INSTRUCCION-XXX.md`

### PASO 6: Confirmar Estado en Log

Escribir en log de inicio (o en comentario de commit):

```
=== INICIO DE SESIÓN ODIN ===
Fecha: {YYYY-MM-DD HH:MM}
Soy ODIN. Proyectos físicos detectados: {lista}
Proyecto activo: {X}
Módulo activo: {Y}
Instrucción vigente: {Z}
Estado módulo anterior: {VALIDADO / EN CORRECCIÓN / NO INICIADO}
Metodología: {ODIN-TRAD / ODIN-IA / Ambas}
Último commit: {hash}
Listo para trabajar.
=== FIN INICIO ===
```

---

## 🆘 SECCIÓN ESPECIAL: PERDISTE CONTEXTO (Cerraste VS Code, nueva ventana, etc.)

**Si cerraste la ventana de VS Code donde estaba Kimi Code, o iniciaste nueva sesión, o no recuerdas en qué módulo estás: Sigue este protocolo de emergencia.**

### Protocolo de Recuperación de Contexto (5 minutos)

```bash
# 1. Sincronizar repo
 cd ~/Desarrollos  # o tu ruta local
 git pull origin setup/estructura-2026

# 2. Leer documento de gobierno (ESTE ES EL MÁS IMPORTANTE)
 cat metodologia/GOBIERNO-ZEUS-ODIN.md

# 3. Leer estado maestro (subir al directorio padre de Desarrollos, entrar a IDC_PROYECTOS)
 cd ../IDC_PROYECTOS  # o tu ruta
 cat SINCRONIZACION-MAESTRA.md

# 4. Leer instrucción vigente
 ls INSTRUCCIONES/
 cat INSTRUCCIONES/INSTRUCCION-ODIN-004-EXCEPCION.md

# 5. Confirmar en chat:
# "Soy ODIN. Leí GOBIERNO-ZEUS-ODIN.md y SINCRONIZACION-MAESTRA.md.
#  Estado actual: Módulo 005 y 006 AUTORIZADOS. Proyecto 005 activo.
#  Listo para trabajar según INSTRUCCION-ODIN-004-EXCEPCION.md."
```

**Documentos MÍNIMOS que debes leer si perdiste contexto:**
1. `GOBIERNO-ZEUS-ODIN.md` (5 minutos) — entiendes quién eres, qué puedes hacer, qué NO puedes hacer
2. `SINCRONIZACION-MAESTRA.md` (2 minutos) — sabes qué módulo está en qué estado
3. `INSTRUCCION-ODIN-004-EXCEPCION.md` (3 minutos) — sabes qué te pidieron hacer

**Total: 10 minutos. Luego puedes empezar a codear con certeza.**

**NO EMPIECES A CODEAR sin leer estos 3 documentos. Si no los lees, no sabes qué estado tiene el proyecto y puedes repetir trabajo o romper algo que ya estaba validado.**

## MAPA DE DOCUMENTOS (Dónde está cada cosa)

| Documento | Ubicación | Quién lo actualiza | Propósito | ¿Cuándo leer? |
|-----------|-----------|-------------------|-----------|---------------|
| **GOBIERNO-ZEUS-ODIN.md** | `Desarrollos/metodologia/` | ZEUS | **Documento de gobierno maestro.** Reglas, flujo, roles, repos, candados | **SIEMPRE al iniciar si perdiste contexto** |
| AGENTS.md | `Desarrollos/metodologia/` | ZEUS (modifica), Jelkin (aprueba) | Identidad y límites de ODIN | Primera vez, luego referencia |
| **SINCRONIZACION-MAESTRA.md** | `IDC_PROYECTOS/` | ZEUS | **Estado REAL de todos los módulos y proyectos** | **SIEMPRE al iniciar** |
| INSTRUCCION-XXX.md | `IDC_PROYECTOS/INSTRUCCIONES/` | ZEUS (genera), Jelkin (firma) | Instrucción formal para ODIN | Cuando existe, antes de codear |
| INICIO-SESION-ODIN.md | `Desarrollos/metodologia/` | ZEUS | Este checklist | Referencia cuando olvidas pasos |
| ACTA-VALIDACION-XXX.md | `Desarrollos/PROYECTO-XXX/docs/auditoria/` | ZEUS | Comprobante de validación | Cuando ODIN dice "listo", ZEUS lo genera |
| ACTA-CORRECCION-XXX.md | `Desarrollos/PROYECTO-XXX/docs/auditoria/` | ZEUS | Acciones correctivas | Cuando validación rechaza |
| SELECTOR-METODOLOGIA.md | `Desarrollos/metodologia/` | ZEUS | Proyectos existentes | Contexto histórico, no crítico |
| ODIN-TRAD.md | `Desarrollos/metodologia/` | ZEUS | Metodología desarrollo tradicional | Obsoleto, reemplazado por GOBIERNO |

### ¿Qué documentos son CRÍTICOS y cuáles son de referencia?

**CRÍTICOS (leer SIEMPRE si perdiste contexto):**
1. GOBIERNO-ZEUS-ODIN.md (5 min)
2. SINCRONIZACION-MAESTRA.md (2 min)
3. INSTRUCCION-XXX.md (si existe) (3 min)

**DE REFERENCIA (leer si tienes dudas específicas):**
4. AGENTS.md — si olvidaste tus límites
5. INICIO-SESION-ODIN.md — si olvidaste el checklist
6. ACTA-VALIDACION/CORRECCION — si ZEUS te lo pide

**OBSOLETOS (no leer salvo contexto histórico):**
7. SELECTOR-METODOLOGIA.md
8. ODIN-TRAD.md

---

## QUÉ HACER SI ALGO FALLA

| Situación | Acción | NOTIFICAR A |
|-----------|--------|-------------|
| Repo no sincroniza | `git status` → verificar conflictos → NOTIFICAR | ZEUS |
| Proyecto en matriz pero no en disco | DETENER. No crear carpeta. | Jelkin + ZEUS |
| Instrucción no existe | NO empezar módulo. Esperar. | Jelkin |
| Instrucción es para módulo ya validado | Confirmar con Jelkin. | Jelkin |
| Tests fallan en repo limpio | `git status` → verificar rama → NOTIFICAR | ZEUS |
| No entiendo qué hacer | Leer GOBIERNO-ZEUS-ODIN.md. Si sigue sin claro: | ZEUS + Jelkin |

---

## EJEMPLO DE INICIO DE SESIÓN COMPLETO (Estado actual: 14 de junio 2026, 23:45 CST)

```bash
# PASO 1: Sincronizar
cd ~/Desarrollos
git pull origin setup/estructura-2026
# OK: Already up to date.

# PASO 2: Leer documentos de gobierno (SIEMPRE si perdiste contexto)
# (ODIN lee GOBIERNO-ZEUS-ODIN.md, AGENTS.md, ../SINCRONIZACION-MAESTRA.md)

# PASO 3: Verificar proyectos
ls -d PROYECTO-*/
# PROYECTO-005-PROTECCION-INFANTIL/

# PASO 4: Verificar estado (subir a IDC_PROYECTOS)
cd ../IDC_PROYECTOS
cat SINCRONIZACION-MAESTRA.md
# Módulo 001: VALIDADO v2 (ACTA-VALIDACION-ODIN-001-v2.md)
# Módulo 002: VALIDADO (ACTA-VALIDACION-ODIN-002.md)
# Módulo 003: VALIDADO (ACTA-VALIDACION-ODIN-003.md)
# Módulo 004: VALIDADO CON EXCEPCIÓN (3 deudas técnicas, 21 junio)
# Módulo 005: AUTORIZADO (INSTRUCCION-ODIN-004-EXCEPCION.md)
# Módulo 006: AUTORIZADO (INSTRUCCION-ODIN-004-EXCEPCION.md)

# PASO 5: Verificar instrucción
ls INSTRUCCIONES/
# INSTRUCCION-ODIN-004-EXCEPCION.md (firmada por Jelkin, 2026-06-14)
# "ODIN: Desarrollar Módulos 5 y 6 sin bloqueo de 004. DoD obligatorio."

# PASO 6: Confirmar en chat
# "Soy ODIN. Leí GOBIERNO-ZEUS-ODIN.md y SINCRONIZACION-MAESTRA.md.
#  Proyecto activo: PROYECTO-005. Módulos: 005 y 006 (AUTORIZADOS).
#  Instrucción: INSTRUCCION-ODIN-004-EXCEPCION.md. Listo para trabajar.
#  Último commit: {hash}. Estado: 4 módulos validados, 2 autorizados."
```

---

> **"No empieces a codear sin saber dónde estás. Este checklist te dice dónde estás."**
> **ZEUS — CEO PMO**
