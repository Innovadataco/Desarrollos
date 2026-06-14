# Semáforo de Confianza

## Plataforma de Protección Infantil Comunitaria

**Proyecto:** 005 — Innovadataco  
**Código:** IDC_2026_05  
**Versión:** 2.0 (Pivote PWA + Semáforo de Confianza)  
**Fecha:** 13 de junio de 2026  

---

## 🎯 Visión

> **Un buscador universal de confianza donde cualquier persona puede consultar si un número de teléfono, cuenta de redes sociales o correo electrónico ha sido reportado como riesgo para menores, y reportar contactos inapropiados sin exponer su identidad.**

---

## 🚦 ¿Qué es el Semáforo de Confianza?

Cada identificador consultado muestra un **semáforo de confianza comunitaria**:

| Color | Significado | Estado |
|-------|------------|--------|
| 🟢 **Verde** | Sin reportes. Sin señales de riesgo. | Libre |
| 🟡 **Amarillo** | 1-2 reportes leves. Precaución. | Precaución |
| 🔴 **Rojo** | 3+ reportes o patrones de riesgo detectados. | Alerta |
| ⚫ **Negro** | Red organizada detectada (mismo ID desde ≥3 ciudades/países). | Riesgo Crítico |

**El semáforo NO acusa.** Es una señal comunitaria de confianza. La investigación y acción legal son responsabilidad exclusiva de las autoridades competentes.

---

## 🏗️ Arquitectura de Módulos

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         USUARIO (Navegador Móvil/Web)                     │
│                   Sin login, sin cookies, sin IP guardada                │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │ HTTPS
                           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  FRONTEND — PWA (React 19 + Vite + Tailwind CSS)                        │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐             │
│  │ Consulta        │ │ Reporte         │ │ Panel Admin     │             │
│  │ Semáforo        │ │ Anónimo         │ │ (Auth JWT)      │             │
│  │ (Pública)       │ │ (Pública)       │ │ (Protegido)     │             │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘             │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  BACKEND — FastAPI + SQLAlchemy + PostgreSQL                            │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 001: Registro Anónimo (🚧 EN CORRECCIÓN / NO VALIDADO)      │  │
│  │ POST /api/reportes — Encriptación AES-256-GCM, rate limiting    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 002: Consulta Semáforo (NUEVO)                           │  │
│  │ GET /api/validate/{identifier} — Estadísticas agregadas         │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 003: IA Triage (NUEVO)                                   │  │
│  │ NLP para clasificación de reportes + detección grooming        │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 004: Clustering + Perfil Agresor (NUEVO)                │  │
│  │ Geográfico, timeline, detección de red organizada                │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 005: Panel Admin (NUEVO)                                │  │
│  │ Dashboard, auth, desencriptación, export                         │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ MÓDULO 006: Pasarela Institucional (NUEVO)                      │  │
│  │ API gateway, Te Protejo, NCMEC, formatos estándar                │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  INFRAESTRUCTURA                                                        │
│  • PostgreSQL 16 (datos encriptados)                                    │
│  • Redis (rate limiting + cache + sesiones admin)                       │
│  • Docker + Docker Compose                                              │
│  • GitHub Actions CI/CD                                                 │
│  • VPS Cloud (DigitalOcean / Hetzner / AWS Lightsail)                   │
│  • Nginx reverse proxy + TLS 1.3 (Let's Encrypt)                        │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Principios de Seguridad y Privacidad

1. **Anonimato Absoluto:** Sin IP, sin cookies, sin localStorage, sin user-agent, sin metadata. Solo el navegador y el servidor. Nada más.
2. **Encriptación Industrial:** AES-256-GCM con DEK (Data Encryption Key) único por campo. Las claves maestras nunca tocan el disco de producción.
3. **Sin Juicio:** El sistema nunca dice "este es un pedófilo". Dice: "este identificador tiene X reportes de contacto inapropiado con menores, detectado por la comunidad".
4. **Evidencia Protegida:** Fotos, videos, capturas de pantalla y audios encriptados con AES-256-GCM. Solo desencriptables bajo demanda por admin autorizado con audit trail.
5. **Legalmente Conservador:** No scoring de pedofilia, no evidencia pública, no alertar al agresor. La plataforma es un canal tecnológico, no un operador judicial.

---

## 💰 Modelo de Negocio

### Freemium B2C

| Plan | Precio | Funcionalidad |
|------|--------|---------------|
| **Gratuito** | $0 | 3 consultas/día, reportes anónimos ilimitados |
| **Premium** | $2.99/mes | Consultas ilimitadas, alertas por email, historial de reportes |

### B2B2C — Instituciones Educativas

| Plan | Precio | Funcionalidad |
|------|--------|---------------|
| **Colegio Básico** | $1,000/año | Panel de consulta para padres, reportes ilimitados, alertas institucionales |
| **Colegio Premium** | $2,500/año | Todo Básico + API de integración, dashboard de tendencias, soporte prioritario |
| **Distrito Educativo** | Custom | Multi-colegio, analytics agregado, pasarela directa con autoridades |

---

## 📱 ¿Por qué PWA y no App Store?

- **Sin fricción:** El usuario accede desde el navegador. Sin descarga, sin tienda, sin aprobación.
- **Anonimato perfecto:** Sin SDKs de tracking, sin permisos de dispositivo, sin metadata de instalación.
- **Velocidad:** No esperar 3-5 días de revisión de Apple/Google para cada actualización.
- **Costo:** $0 de licencia de desarrollador, $0 de comisiones de tienda.
- **Latinoamérica:** En muchos mercados, la gente no usa App Store. Usa WhatsApp Web y navegador móvil.

---

## 🚀 Stack Técnico

| Capa | Tecnología | Versión |
|------|------------|---------|
| Frontend | React 19 + Vite + Tailwind CSS | 19.x |
| PWA | Workbox + Service Worker | 7.x |
| Backend | FastAPI + SQLAlchemy | 0.115+ |
| Base de datos | PostgreSQL | 16.x |
| Cache/Rate limiting | Redis | 7.x |
| Encriptación | Python cryptography (AES-256-GCM) | 43.x |
| IA/ML | scikit-learn + transformers (Hugging Face) | 1.5+ / 4.x |
| Container | Docker + Docker Compose | 27.x |
| CI/CD | GitHub Actions | — |
| Deploy | VPS cloud + Nginx | — |

---

## 📁 Estructura de Especificaciones (SDD)

```
specs/
├── 001-registro-anonimo/          # Módulo 001 (🚧 EN CORRECCIÓN / NO VALIDADO)
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── 002-consulta-semaforo/          # Módulo 002 (NUEVO)
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── 003-ia-triage/                  # Módulo 003 (NUEVO)
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── 004-clustering-perfil/          # Módulo 004 (NUEVO)
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
├── 005-panel-admin/                # Módulo 005 (NUEVO)
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
└── 006-pasarela-institucional/     # Módulo 006 (NUEVO)
    ├── spec.md
    ├── plan.md
    └── tasks.md

docs/
├── gaps.md                         # Gaps resueltos y pendientes
├── ADR-001-seguridad.md            # Decisión: encriptación AES-256-GCM
├── ADR-002-pwa.md                  # Decisión: PWA vs App Store
├── ADR-003-ia-triage.md            # Decisión: modelo NLP + dataset
├── ADR-004-clustering.md           # Decisión: algoritmo clustering + privacidad
├── ADR-005-pasarela.md             # Decisión: integración con autoridades
├── estructura-datos.md             # Esquema SQL completo
└── api-reference.md                # Documentación de endpoints
```

---

## 🎯 Fases y Timeline

| Fase | Módulo | Fecha | Estado | Horas |
|------|--------|-------|--------|-------|
| 1 | 001 Registro Anónimo | Junio 2026 | 🚧 En corrección — pendiente validación ZEUS | 40h |
| 2 | 002 Consulta Semáforo | Julio 2026 | ⬜ Nuevo | 36h |
| 3 | 003 IA Triage | Agosto 2026 | ⬜ Nuevo | 48h |
| 4 | 004 Clustering + Perfil | Septiembre 2026 | ⬜ Nuevo | 54h |
| 5 | 005 Panel Admin | Octubre 2026 | ⬜ Nuevo | 50h |
| 6 | 006 Pasarela Institucional | Noviembre 2026 | ⬜ Nuevo | 48h |
| 7 | Producción + Piloto | Diciembre 2026 | ⬜ Nuevo | 78h |
| **Total** | | | | **354h** |

---

## 👥 Equipo

| Rol | Responsable | Tiempo |
|-----|-------------|--------|
| Desarrollo Full-Stack | ODIN (Kimi Code CLI) | 100% |
| Gestión de Proyecto / PMO | ZEUS (AI Agent) | 20% |
| Revisión Legal / Compliance | Diana (Cofundadora) | 10% |
| Marketing / Posicionamiento | Zaira | 10% |
| Soporte Técnico / Backup | Juan | 10% |

---

## 📜 Licencia y Legal

- **Código:** Licencia AGPL v3 (open source, copyleft, auditable).
- **Operación:** Innovadataco es canal tecnológico. No investiga, no juzga, no alerta al agresor.
- **Responsabilidad:** Definida contractualmente en contratos con autoridades. Innovadataco no asume responsabilidad penal de operación sin contrato explícito.

---

> *Documento generado por ZEUS — Innovadataco*  
> *Versión 2.0 — Pivote Semáforo de Confianza*  
> *ZEUS online. La empresa está operando.* ⚡
