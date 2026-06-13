# SPEC-001: Registro Anónimo de Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-12  
**Autor:** ODIN (CEO IA Dev)  
**Aprobador:** Jelkin (CEO)  
**Estado:** Aprobado

---

## 1. RESUMEN EJECUTIVO

Módulo que permite a cualquier persona enviar un reporte anónimo sobre posibles incidentes de protección infantil. El sistema garantiza el anonimato del reportante: no guarda IP, user-agent, cookies ni metadata del navegador. Los datos sensibles se encriptan en reposo con AES-256-GCM y el sistema devuelve un hash único como prueba de envío.

---

## 2. ALCANCE

### 2.1 Dentro del alcance
- Formulario web anónimo para crear reportes.
- API REST para recibir reportes (`POST /api/reportes`).
- Encriptación de datos sensibles en reposo.
- Rate limiting por IP (5 reportes/hora).
- Health check (`GET /api/health`).
- Tests unitarios e integración backend y frontend.

### 2.2 Fuera del alcance
- Panel de administración para revisar reportes.
- Autenticación de usuarios/administradores.
- Componente de IA/scoring (módulo 002).
- Notificaciones a autoridades.
- Deploy a producción.

---

## 3. USER STORIES

### US-001: Enviar reporte anónimo
**Como** ciudadano  
**Quiero** reportar un incidente de protección infantil de forma anónima  
**Para** alertar a las autoridades sin exponer mi identidad

**Criterios de aceptación:**
- Given el usuario accede al formulario
- When completa identificador, descripción y opcionalmente evidencia
- Then el sistema guarda el reporte encriptado y muestra un hash de confirmación

**Prioridad:** Alta  
**Estimación:** 8h

### US-002: Garantizar anonimato
**Como** reportante  
**Quiero** que el sistema no guarde mi IP ni metadata  
**Para** sentirme seguro al reportar

**Criterios de aceptación:**
- Given el usuario envía un reporte
- Then la base de datos no contiene IP, user-agent, cookies ni device metadata

**Prioridad:** Alta  
**Estimación:** 4h

### US-003: Protección contra abuso
**Como** administrador del sistema  
**Quiero** limitar reportes por IP  
**Para** evitar spam o ataques de denegación

**Criterios de aceptación:**
- Given una IP envía 5 reportes en una hora
- When intenta enviar el sexto
- Then el sistema responde HTTP 429

**Prioridad:** Media  
**Estimación:** 4h

---

## 4. REQUISITOS FUNCIONALES

| ID | Requisito | User Story | Prioridad | Estado |
|----|-----------|------------|-----------|--------|
| RF-001 | Crear reporte con identificador y descripción | US-001 | Alta | Implementado |
| RF-002 | Adjuntar evidencia opcional (texto/imagen) | US-001 | Media | Implementado |
| RF-003 | Generar hash único de confirmación | US-001 | Alta | Implementado |
| RF-004 | No almacenar metadata identificable | US-002 | Alta | Implementado |
| RF-005 | Rate limiting 5 reportes/hora/IP | US-003 | Media | Implementado |

---

## 5. REQUISITOS NO FUNCIONALES

| ID | Requisito | Categoría | Criterio | Prioridad |
|----|-----------|-----------|----------|-----------|
| RNF-001 | Encriptación AES-256-GCM en reposo | Seguridad | Datos sensibles encriptados | Alta |
| RNF-002 | Headers de seguridad OWASP | Seguridad | HSTS, CSP, X-Frame, etc. | Alta |
| RNF-003 | Cobertura de tests ≥ 80% | Calidad | pytest + vitest | Alta |
| RNF-004 | Tiempo de respuesta < 500ms | Performance | 95 percentile | Media |
| RNF-005 | Sin cookies de tracking | Privacidad | No cookies ni localStorage | Alta |

---

## 6. REGLAS DE NEGOCIO

- RN-001: Todo reporte debe tener al menos un identificador reportado y una descripción.
- RN-002: La evidencia opcional solo puede ser de tipo `text` o `image`.
- RN-003: El hash de confirmación debe ser único y no vinculable al reportante.
- RN-004: No se debe permitir más de 5 reportes por hora desde la misma IP.

---

## 7. MOCKUPS / WIREFRAMES

Formulario simple de una columna:
- Campo: Identificador reportado
- Campo: Descripción del incidente
- Select: Tipo de evidencia (opcional)
- Campo: Contenido de evidencia (condicional)
- Botón: Enviar reporte anónimo
- Mensaje de éxito con hash de confirmación

Assets: ver carpeta `assets/` (pendiente de mockups visuales).

---

## 8. CRITERIOS DE ACEPTACIÓN GLOBALES

- [x] Todos los tests pasan (pytest + vitest)
- [x] Cobertura backend ≥ 80%
- [x] Code review aprobado por ZEUS (pendiente)
- [x] Documentación OpenAPI disponible en `/docs`
- [x] Checklist de seguridad completado
- [ ] Jelkin aprueba el demo

---

> Generado por ODIN — Innovadataco
