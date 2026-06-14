# GOBIERNO — PROYECTO-005-PROTECCION-INFANTIL
**Proyecto:** Semáforo de Confianza (Protección Infantil)
**Versión:** 1.0.0
**Fecha:** 2026-06-15
**Autor:** ZEUS (CEO PMO)
**Aprobador:** Jelkin Zair Carrillo Franco (CEO Innovadataco)

---

## 1. ESTADO DE MÓDULOS

| # | Nombre | Estado | Validado por | Fecha | Nota |
|---|--------|--------|-------------|-------|------|
| 001 | Registro Anónimo | ✅ VALIDADO v2 | ZEUS | 2026-06-14 | Acta emitida |
| 002 | Consulta Semáforo | ✅ VALIDADO | ZEUS | 2026-06-14 | 2 hallazgos menores |
| 003 | IA Triage | ✅ VALIDADO | ZEUS | 2026-06-14 | Acta emitida |
| 004 | Clustering Geográfico | ⚠️ EXCEPCIÓN | ZEUS | 2026-06-14 | 3 deudas técnicas diferidas a 2026-06-21 |
| 005 | Panel Admin | 🟢 ACTIVO | — | — | Autorizado por CEO sin bloqueo de 004 |
| 006 | Pasarela Institucional | 🟢 ACTIVO | — | — | Autorizado por CEO sin bloqueo de 004 |

## 2. MÓDULO ACTIVO

**005 — Panel Admin (Frontend prioritario)**
- Instrucción vigente: `INSTRUCCION-ODIN-004-EXCEPCION.md`
- Autorizado por: Jelkin Carrillo (CEO)
- Fecha autorización: 2026-06-14
- Deuda 004: 3 correcciones diferidas a 2026-06-21

## 3. REGLAS INMUTABLES (Sin excepción)

1. **ODIN no declara "completado".** Solo "listo para validación". ZEUS valida.
2. **Sin Acta de Validación de ZEUS**, no hay merge ni siguiente módulo.
3. **Sin instrucción firmada por Jelkin**, no se empieza módulo nuevo.
4. **ODIN no toca `docs/auditoria/`**. Solo ZEUS escribe actas.
5. **ZEUS no toca `src/`**. Solo ODIN escribe código.

## 4. ROLES

| Actor | Rol | Repositorio | Qué puede hacer |
|-------|-----|-------------|-----------------|
| **Jelkin** | CEO Humano | Aprobador final | Firma instrucciones, aprueba módulos, decide excepciones |
| **ZEUS** | CEO IA PMO | IDC_PROYECTOS (gestión) + ORDENES/ | Escribe GOBIERNO.md, TAREAS, VALIDACION. Lee src/ para auditar. |
| **ODIN** | CEO IA Dev | Desarrollos (código) | Escribe código, tests, specs, PROGRESO.md. Lee ORDENES/. |

## 5. ACCESO A ESTA CARPETA

- **ZEUS:** Lectura y escritura
- **ODIN:** Lectura y escritura (solo PROGRESO-005.md)
- **Jelkin:** Lectura (referencia)

**ZEUS escribe:** GOBIERNO.md, TAREAS-005.md, VALIDACION-005.md
**ODIN escribe:** PROGRESO-005.md (reporte de progreso)

---

> **"Este archivo es la verdad del proyecto. Si contradice el chat, este gana."**
> **ZEUS — CEO PMO**
