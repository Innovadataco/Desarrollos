# SELECTOR-METODOLOGIA
## Innovadataco — Selector de Metodología de Desarrollo
**Versión:** 1.3.0  
**Propósito:** Decidir qué metodología aplica a cada proyecto  
**Responsable:** ZEUS (con validación de Jelkin)  
**Ejecutor:** ODIN

---

## 1. REGLA FUNDAMENTAL

> **SOLO existen los proyectos que tienen carpeta física en el repo.**
> 
> ODIN debe ejecutar `ls -d PROYECTO-*/` ANTES de cualquier acción.
> Si la carpeta no existe, el proyecto no existe. ODIN no la crea.
> 
> **ZEUS crea las carpetas. ODIN trabaja dentro de ellas.**

---

## 2. ÁRBOL DE DECISIÓN

```
¿Existe la carpeta PROYECTO-NNN-NOMBRE/ en el repo?
│
└─ NO → PROYECTO NO EXISTE. Detener. Notificar a ZEUS/Jelkin.

   SI → ¿El proyecto tiene un componente de IA que aprende de datos?
        │
        ├─ SÍ → ¿Es el componente IA el CORE del producto (>50% valor)?
        │   │
        │   ├─ SÍ → Aplica ODIN-IA (completo)
        │   │
        │   └─ NO → Aplica ODIN-TRAD + ODIN-IA (componente)
        │       Ejemplo: Proyecto 005 (Protección Infantil) aplica esta categoría.
        │
        └─ NO → ¿Es un MVP rápido de validación (< 2 meses)?
            │
            ├─ SÍ → Aplica ODIN-TRAD (MVP)
            │   Stack: Next.js + Prisma + PostgreSQL (Neon/Vercel)
            │
            └─ NO → Aplica ODIN-TRAD (completo)
                Stack: React + FastAPI + PostgreSQL + Docker
```

---

## 3. MATRIZ DE PROYECTOS (REALIDAD DEL DISCO - 2026-06-12)

| ID | Proyecto | Cliente | ¿IA? | % IA | Metodología | Stack | Estado | Carpeta | ¿Existe? |
|----|----------|---------|------|------|-------------|-------|--------|---------|----------|
| 001 | APP Chía-Girardot | TransConsult | No | 0% | ODIN-TRAD | React + FastAPI + PostGIS | [PENDIENTE] | `PROYECTO-001-APP-CHIA-GIRARDOT/` | ❌ NO |
| 002 | SICOM | MinMinas | No | 0% | PM2 (ZEUS) | [PENDIENTE] | [PENDIENTE] | `PROYECTO-002-SICOM/` | ❌ NO |
| 003 | Taxi Bogotá | [PENDIENTE] | No | 0% | ODIN-TRAD (MVP) | Next.js + Prisma | [PENDIENTE] | `PROYECTO-003-TAXI-BOGOTA/` | ❌ NO |
| 004 | SETP Sincelejo | [PENDIENTE] | No | 0% | ODIN-TRAD | React + FastAPI + PostGIS | [PENDIENTE] | `PROYECTO-004-SETP-SINCELEJO/` | ❌ NO |
| 005 | Protección Infantil | Innovadataco | Sí | 20% | ODIN-TRAD + ODIN-IA | React + FastAPI + PostgreSQL | **EN DESARROLLO** | `PROYECTO-005-PROTECCION-INFANTIL/` | ✅ SÍ |

### 3.1 Estado de los proyectos

- **Proyecto 005:** Único proyecto con carpeta física en el repo. Estado: EN DESARROLLO.
- **Proyectos 001-004:** NO tienen carpetas físicas. Estado: [PENDIENTE].
  - Estos proyectos están planificados pero NO activos.
  - ZEUS debe crear las carpetas cuando Jelkin dé la orden.
  - ODIN NO debe trabajar en ellos hasta que existan físicamente.

### 3.2 Agregar proyecto N+1 (SOLO ZEUS)

Cuando Jelkin/ZEUS decidan activar un nuevo proyecto:

1. **ZEUS crea la carpeta física:** `mkdir PROYECTO-NNN-NOMBRE/`
2. ZEUS actualiza esta matriz (fila N+1) en AGENTS.md y SELECTOR-METODOLOGIA.md
3. ZEUS genera artefactos PM2 en `PROYECTO-NNN-NOMBRE/docs/pm2/`
4. ODIN detecta la nueva carpeta al leer AGENTS.md
5. ODIN lee esta matriz + SELECTOR.md → Aplica metodología
6. ODIN crea estructura `specs/` dentro de la carpeta existente

**ODIN NUNCA crea la carpeta raíz del proyecto. ZEUS la crea.**

---

## 4. INSTRUCCIÓN PARA ODIN

Al iniciar cualquier sesión, ODIN debe:

1. **Verificar físicamente:** `ls -d PROYECTO-*/` o equivalente
2. Leer este archivo (SELECTOR-METODOLOGIA.md)
3. Identificar el proyecto en la matriz
4. **Si no está en la matriz O no tiene carpeta → DETENER.** Solicitar a Jelkin/ZEUS.
5. Leer la metodología correspondiente:
   - `metodologia/ODIN-TRAD.md`
   - `metodologia/ODIN-IA.md`
   - O ambas
6. Confirmar en el chat: "Proyectos físicos detectados: {lista}. Proyecto activo: {X}. Metodología: {Y}."

---

## 5. CAMBIO DE METODOLOGÍA

Si durante el proyecto se detecta que la metodología inicial fue incorrecta:

1. ZEUS detecta el cambio (ej: se agrega módulo de IA a un proyecto tradicional)
2. ZEUS crea GitHub Issue: "Cambio de metodología: {proyecto}"
3. Jelkin aprueba o rechaza
4. Si aprueba: ZEUS actualiza este archivo + genera artefactos PM2 faltantes
5. ODIN ajusta el plan técnico y continúa

---

## 6. HISTORIAL DE CAMBIOS

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | 2026-06-12 | ODIN | Creación inicial. Árbol de decisión + matriz. |
| 1.3.0 | 2026-06-12 | ODIN | **CRÍTICO:** Agregada regla fundamental de carpetas físicas. Matriz actualizada con columna "¿Existe?". Solo 005 = ✅. |

---

> "La metodología correcta es la que entrega valor al cliente, no la que es más cool."
> **SELECTOR-METODOLOGIA — Innovadataco**
