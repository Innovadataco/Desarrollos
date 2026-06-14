# GUÍA JELKIN — ¿Qué hacer cuando ODIN pierde contexto?
**Versión:** 1.0.0
**Fecha:** 2026-06-15
**Autor:** ZEUS (CEO PMO)
**Para:** Jelkin Zair Carrillo Franco (CEO Innovadataco)

---

## ❓ ¿Qué es "perder contexto"?

ODIN (Kimi Code en VS Code) **no tiene memoria** entre sesiones. Si:
- Cierra VS Code
- Apaga la computadora
- Abre una nueva ventana de Kimi
- Pierde conexión

...entonces ODIN **olvida todo**. No sabe en qué proyecto está, qué módulo tocaba, ni qué tarea estaba haciendo.

**Solución: Tú le das 2 líneas.** ODIN lee los archivos que ZEUS preparó y recupera todo.

---

## ✅ ACCIÓN: 2 Líneas que pegas en Kimi

Cuando ODIN "está perdido", abre Kimi y pega EXACTAMENTE esto:

```
ODIN, lee el archivo PROYECTO-005-PROTECCION-INFANTIL/ORDENES/GOBIERNO.md 
y dime qué módulo está activo y qué tareas hay pendientes.
```

**Eso es todo.** ODIN leerá el archivo, sabrá que el Módulo 005 está activo, y pedirá las tareas.

---

## 🔄 FLUJO COMPLETO (Paso a paso)

### Paso 1 — ODIN está perdido

ODIN dice: "¿En qué proyecto estoy? ¿Qué debo hacer?"

### Paso 2 — Tú pegas las 2 líneas

```
ODIN, lee el archivo PROYECTO-005-PROTECCION-INFANTIL/ORDENES/GOBIERNO.md 
y dime qué módulo está activo y qué tareas hay pendientes.
```

### Paso 3 — ODIN lee GOBIERNO.md

ODIN responde algo como:
```
Soy ODIN. Leí GOBIERNO.md:
- Módulo activo: 005 — Panel Admin
- Estado: AUTORIZADO por CEO el 2026-06-14
- Tareas: 26 items pendientes
- Prioridad: Frontend (Dashboard, ReportsList, ReportDetail)
```

### Paso 4 — Tú le dices que siga

```
Perfecto. Lee TAREAS-005.md y empieza a desarrollar.
Reporta tu progreso en PROGRESO-005.md.
```

### Paso 5 — ODIN trabaja solo

ODIN lee TAREAS-005.md, desarrolla, y reporta en PROGRESO-005.md. Tú no tienes que hacer nada más.

---

## 📋 CHECKLIST RÁPIDO

| Situación | Qué haces tú | Qué hace ODIN | Qué revisa ZEUS |
|-----------|-------------|---------------|-----------------|
| ODIN pierde contexto | Pegas 2 líneas | Lee GOBIERNO.md + TAREAS | — |
| ODIN dice "terminé una tarea" | Nada (ODIN reporta solo) | Escribe en PROGRESO-005.md | Valida cuando pueda |
| ODIN dice "terminé el módulo" | Nada | Escribe "LISTO PARA VALIDACION" | ZEUS audita en VALIDACION-005.md |
| ZEUS dice "módulo validado" | Nada | Lee VALIDACION-005.md | ZEUS actualiza GOBIERNO.md → siguiente módulo |
| Quieres que ODIN pase al módulo 6 | Nada (ZEUS ya actualizó GOBIERNO.md) | Lee GOBIERNO.md → ve "006 ACTIVO" | — |

---

## 🎯 PROMPT GENÉRICO (Para CUALQUIER proyecto)

Si no recuerdas el número del proyecto, usa este prompt genérico:

```
ODIN, busca la carpeta ORDENES/ dentro del proyecto que estás trabajando 
y lee el archivo GOBIERNO.md. Dime qué módulo está activo.
```

ODIN buscará el archivo y te dirá.

---

## ⚠️ ¿Qué NO hacer?

| ❌ NO hagas esto | ✅ En su lugar |
|------------------|---------------|
| "ODIN, recuerda que estabas haciendo el dashboard" | "ODIN, lee GOBIERNO.md" |
| "ODIN, el módulo 5, el panel admin, las tareas..." | "ODIN, lee TAREAS-005.md" |
| Escribir un prompt de 500 líneas | Pegar las 2 líneas de arriba |
| Tratar de reconstruir el contexto tú mismo | Dejar que ODIN lea los archivos |

---

## 📁 ¿Dónde están los archivos?

En el repo de Desarrollos, dentro de cada proyecto:

```
Desarrollos/
└── PROYECTO-005-PROTECCION-INFANTIL/
    └── ORDENES/
        ├── GOBIERNO.md          ← ODIN lee esto primero
        ├── TAREAS-005.md        ← Lista de tareas
        ├── PROGRESO-005.md      ← ODIN reporta aquí
        └── VALIDACION-005.md    ← ZEUS audita aquí
```

**Cada proyecto tiene su propia carpeta ORDENES/.**

---

## 🆘 EMERGENCIA: Si ODIN no encuentra el archivo

Si ODIN dice "no encuentro GOBIERNO.md", prueba este prompt:

```
ODIN, ejecuta esto en tu terminal:
find ~ -name "GOBIERNO.md" -type f 2>/dev/null | head -5
Dime qué rutas encontraste.
```

ODIN buscará el archivo y te dirá dónde está.

---

> **"2 líneas. Eso es todo lo que necesitas."**
> **ZEUS — CEO PMO**
