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

### PASO 2: Leer Documentos de Gobierno (en orden)

Leer estos documentos SÍ o SÍ antes de tocar código:

1. [ ] **`metodologia/AGENTS.md`** → Recordar quién soy, qué puedo hacer, qué NO puedo hacer
2. [ ] **`metodologia/SELECTOR-METODOLOGIA.md`** → Verificar proyectos físicos existentes
3. [ ] **`metodologia/ODIN-TRAD.md`** o **`ODIN-IA.md`** → Recordar metodología activa
4. [ ] **`GOBIERNO-ZEUS-ODIN.md`** → Recordar flujo de trabajo, reglas de gobierno
5. [ ] **`INICIO-SESION-ODIN.md`** (este archivo) → Confirmar que ejecuté checklist

### PASO 3: Verificar Proyectos Físicos
```bash
ls -d PROYECTO-*/
```
- [ ] Lista de carpetas físicas coincide con `SELECTOR-METODOLOGIA.md`
- [ ] Si hay proyecto en matriz pero NO en disco → DETENER. Notificar a ZEUS/Jelkin.
- [ ] Si hay proyecto en disco pero NO en matriz → NOTIFICAR a ZEUS.

### PASO 4: Verificar Estado Actual

Leer documentos de estado:

1. [ ] **`SINCRONIZACION-MAESTRA.md`** (en IDC_PROYECTOS) → Verificar estado global de todos los proyectos
2. [ ] **`INSTRUCCIONES-ODIN-XXX.md`** (si existe) → Verificar instrucciones pendientes
3. [ ] **`PROYECTO-XXX/docs/auditoria/`** → Verificar actas de validación/corrección

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

## MAPA DE DOCUMENTOS (Dónde está cada cosa)

| Documento | Ubicación | Quién lo actualiza | Propósito |
|-----------|-----------|-------------------|-----------|
| AGENTS.md | Desarrollos/metodologia/ | ZEUS (modifica), Jelkin (aprueba) | Identidad y límites de ODIN |
| SELECTOR-METODOLOGIA.md | Desarrollos/metodologia/ | ZEUS | Proyectos existentes y físicos |
| ODIN-TRAD.md | Desarrollos/metodologia/ | ZEUS | Metodología desarrollo tradicional |
| ODIN-IA.md | Desarrollos/metodologia/ | ZEUS | Metodología desarrollo IA |
| SDD-INNOVADATACO.md | Desarrollos/metodologia/ | ZEUS | Fase ZERO: especificación antes de código |
| GOBIERNO-ZEUS-ODIN.md | Desarrollos/ | ZEUS | Reglas de gobierno, roles, flujo |
| INICIO-SESION-ODIN.md | Desarrollos/metodologia/ | ZEUS | Este checklist |
| SINCRONIZACION-MAESTRA.md | IDC_PROYECTOS/ | ZEUS | Estado global de todos los proyectos |
| INSTRUCCION-XXX.md | IDC_PROYECTOS/INSTRUCCIONES/ | ZEUS (genera), Jelkin (firma) | Instrucción formal para ODIN |
| ACTA-VALIDACION-XXX.md | Desarrollos/PROYECTO-XXX/docs/auditoria/ | ZEUS | Comprobante de validación |
| ACTA-CORRECCION-XXX.md | Desarrollos/PROYECTO-XXX/docs/auditoria/ | ZEUS | Acciones correctivas |

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

## EJEMPLO DE INICIO DE SESIÓN COMPLETO

```bash
# PASO 1: Sincronizar
cd ~/Desarrollos
git pull origin setup/estructura-2026
# OK: Already up to date.

# PASO 2: Leer documentos
# (ODIN lee AGENTS.md, SELECTOR-METODOLOGIA.md, ODIN-TRAD.md)

# PASO 3: Verificar proyectos
ls -d PROYECTO-*/
# PROYECTO-005-PROTECCION-INFANTIL/

# PASO 4: Verificar estado
cat SINCRONIZACION-MAESTRA.md
# Módulo 001: EN CORRECCIÓN (ACTA-CORRECCION-ODIN-001.md)
# Módulo 002: NO INICIADO (espera instrucción)
# Módulo 003: NO INICIADO (espera instrucción)

# PASO 5: Verificar instrucción
ls INSTRUCCIONES/
# INSTRUCCION-ODIN-001.md (firmada por Jelkin, 2026-06-14)
# "ODIN: Corregir bugs del Módulo 001 según ACTA-CORRECCION"

# PASO 6: Confirmar
# "Soy ODIN. Proyecto activo: PROYECTO-005. Módulo: 001 (corrección).
# Instrucción: INSTRUCCION-ODIN-001.md. Listo para trabajar."
```

---

> **"No empieces a codear sin saber dónde estás. Este checklist te dice dónde estás."**
> **ZEUS — CEO PMO**
