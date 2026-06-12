# Metodología — Innovadataco

## Repositorio Oficial
https://github.com/Innovadataco/Desarrollos

## Estructura de Documentos

```
metodologia/
├── AGENTS.md                    ← Documento maestro de ODIN (LEER PRIMERO)
├── ODIN-TRAD.md                 ← Desarrollo tradicional (apps, webs, APIs)
├── ODIN-IA.md                   ← Desarrollo con IA (ML, scoring, NLP)
├── SDD-INNOVADATACO.md          ← Software Development Definition (fase ZERO)
├── SELECTOR.md                  ← Selector simple de metodología
├── SELECTOR-METODOLOGIA.md      ← Árbol de decisión + matriz de proyectos
├── README.md                    ← Este archivo
├── standards/
│   ├── commit-convention.md     ← Reglas de commits
│   ├── code-review.md           ← Checklist de revisión de código
│   └── security-checklist.md    ← Checklist de seguridad OWASP
└── templates/
    ├── ADR-template.md           ← Architecture Decision Record
    ├── plan-template.md          ← Plan técnico
    ├── spec-template.md          ← Especificación funcional
    └── tasks-template.md         ← Desglose de tareas
```

## Flujo de Inicio Rápido

1. **ODIN inicia sesión** → Lee `AGENTS.md`
2. **Selecciona proyecto** → Lee `SELECTOR.md` + `SELECTOR-METODOLOGIA.md`
3. **Selecciona metodología** → Lee `ODIN-TRAD.md` o `ODIN-IA.md`
4. **Inicia SDD** → Lee `SDD-INNOVADATACO.md`
5. **Aplica estándares** → Usa templates y standards

## Límites Claros

| Actor | Puede tocar | NO puede tocar |
|-------|-------------|----------------|
| **ODIN** | `metodologia/`, `PROYECTO-*/src/`, `PROYECTO-*/specs/` | `PROYECTO-*/docs/pm2/` (ZEUS) |
| **ZEUS** | `PROYECTO-*/docs/pm2/`, `metodologia/` (solo lectura para referencia) | `PROYECTO-*/src/` (ODIN) |
| **Jelkin** | Todo (aprobador final) | — |

## Contacto

- **ODIN (CEO IA Dev):** Desarrollo, tests, deploy, code review
- **ZEUS (CEO IA PM2):** Gestión, artefactos PM2, cronograma, riesgos
- **Jelkin (CEO Humano):** Aprobaciones, visión estratégica, escalaciones
- **Puente:** GitHub (Issues, PRs, Actions, Releases)
