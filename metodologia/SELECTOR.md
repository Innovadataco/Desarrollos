# SELECTOR DE METODOLOGÍA
## ¿Qué metodología aplica a cada proyecto?

### Regla simple:
- **¿El proyecto tiene un componente de IA que aprende de datos?** → Aplica ODIN-IA
- **¿El proyecto es una app/web/sistema tradicional sin IA?** → Aplica ODIN-TRAD
- **¿El proyecto tiene ambos?** → Aplica ODIN-TRAD + ODIN-IA (componente IA)

### Mapeo de proyectos Innovadataco:

| Proyecto | Tipo | Metodología | Nota |
|----------|------|-------------|------|
| 001 APP Chía-Girardot | ITS / Web / GIS | **ODIN-TRAD** | Sin IA central |
| 002 SICOM | Operación / Gestión | **Ninguna** (solo PM2) | Empalme operativo |
| 003 Taxi Bogotá | Consultoría / MVP | **ODIN-TRAD** (MVP) | Sin IA |
| 004 SETP Sincelejo | ITS / Sistema recaudo | **ODIN-TRAD** | Sin IA central |
| 005 Protección Infantil | Web + IA (scoring) | **ODIN-TRAD + ODIN-IA** | 80% app + 20% IA |

### Instrucción para ODIN:

Al iniciar un proyecto, Jelkin debe decir:

```
"ODIN, aplica metodología ODIN-TRAD para este proyecto."
```

O:

```
"ODIN, aplica ODIN-TRAD para la app y ODIN-IA para el módulo de scoring."
```

ODIN leerá el documento correspondiente y ejecutará las fases.

---

## Estructura de documentos en el repo:

```
/Desarrollos/
└── metodologia/
    ├── ODIN-TRAD.md          ← Desarrollo tradicional
    ├── ODIN-IA.md            ← Desarrollo con IA
    └── SELECTOR.md           ← Este archivo
```
