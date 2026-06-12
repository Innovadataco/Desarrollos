# SELECTOR-METODOLOGIA
## Innovadataco — Selector de Metodología de Desarrollo
**Versión:** 1.0.0  
**Propósito:** Decidir qué metodología aplica a cada proyecto  
**Responsable:** ZEUS (con validación de Jelkin)  
**Ejecutor:** ODIN

---

## 1. ÁRBOL DE DECISIÓN

```
¿El proyecto tiene un componente de IA que aprende de datos?
│
├─ SÍ → ¿Es el componente IA el CORE del producto (>50% valor)?
│   │
│   ├─ SÍ → Aplica ODIN-IA (completo)
│   │   Ejemplo: Sistema de scoring de riesgo, detección de fraudes,
│   │   clasificación automática de imágenes, NLP para análisis de sentimiento.
│   │
│   └─ NO → Aplica ODIN-TRAD + ODIN-IA (componente)
│       Ejemplo: App web con módulo de recomendación, dashboard con
│       predicciones, formulario con análisis de texto automático.
│       Proyecto 005 (Protección Infantil) aplica esta categoría.
│
└─ NO → ¿Es un MVP rápido de validación (< 2 meses)?
    │
    ├─ SÍ → Aplica ODIN-TRAD (MVP)
    │   Stack: Next.js + Prisma + PostgreSQL (Neon/Vercel)
    │   Ejemplo: Proyecto 003 (Taxi Bogotá) en fase de validación.
    │
    └─ NO → Aplica ODIN-TRAD (completo)
        Stack: React + FastAPI + PostgreSQL + Docker
        Ejemplo: Proyecto 001 (APP Chía-Girardot), Proyecto 004 (SETP).
```

---

## 2. MATRIZ DE PROYECTOS (Escalable)

| ID | Proyecto | Cliente | ¿IA? | % IA | Metodología | Stack | Estado | Carpeta |
|----|----------|---------|------|------|-------------|-------|--------|---------|
| 001 | APP Chía-Girardot | TransConsult | No | 0% | ODIN-TRAD | React + FastAPI + PostGIS | [PENDIENTE] | `PROYECTO-001-APP-CHIA-GIRARDOT/` |
| 002 | SICOM | MinMinas | No | 0% | PM2 (ZEUS) | [PENDIENTE] | [PENDIENTE] | `PROYECTO-002-SICOM/` |
| 003 | Taxi Bogotá | [PENDIENTE] | No | 0% | ODIN-TRAD (MVP) | Next.js + Prisma | [PENDIENTE] | `PROYECTO-003-TAXI-BOGOTA/` |
| 004 | SETP Sincelejo | [PENDIENTE] | No | 0% | ODIN-TRAD | React + FastAPI + PostGIS | [PENDIENTE] | `PROYECTO-004-SETP-SINCELEJO/` |
| 005 | Protección Infantil | Innovadataco | Sí | 20% | ODIN-TRAD + ODIN-IA | React + FastAPI + PostgreSQL | **EN DESARROLLO** | `PROYECTO-005-PROTECCION-INFANTIL/` |

### 2.1 Agregar proyecto N+1

Cuando llegue un nuevo proyecto:

1. Jelkin define: ID, nombre, cliente, tipo de negocio
2. ZEUS evalúa: ¿IA? ¿MVP? ¿Completo?
3. ZEUS actualiza esta matriz (fila N+1)
4. ODIN lee esta matriz + SELECTOR.md → Aplica metodología
5. ODIN crea carpeta `PROYECTO-NNN-NOMBRE/` con estructura inicial

---

## 3. INSTRUCCIÓN PARA ODIN

Al iniciar cualquier proyecto, ODIN debe:

1. Leer este archivo (SELECTOR-METODOLOGIA.md)
2. Identificar el proyecto en la matriz
3. Si no está en la matriz → Solicitar a Jelkin que lo clasifique
4. Leer la metodología correspondiente:
   - `metodologia/ODIN-TRAD.md`
   - `metodologia/ODIN-IA.md`
   - O ambas
5. Confirmar en el chat: "Metodología seleccionada: {X} para Proyecto {Y}"

---

## 4. CAMBIO DE METODOLOGÍA

Si durante el proyecto se detecta que la metodología inicial fue incorrecta:

1. ZEUS detecta el cambio (ej: se agrega módulo de IA a un proyecto tradicional)
2. ZEUS crea GitHub Issue: "Cambio de metodología: {proyecto}"
3. Jelkin aprueba o rechaza
4. Si aprueba: ZEUS actualiza este archivo + genera artefactos PM2 faltantes
5. ODIN ajusta el plan técnico y continúa

---

> "La metodología correcta es la que entrega valor al cliente, no la que es más cool."
> **SELECTOR-METODOLOGIA — Innovadataco**
