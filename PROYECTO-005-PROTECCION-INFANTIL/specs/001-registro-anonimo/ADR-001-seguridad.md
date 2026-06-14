# ADR-001: Seguridad y Anonimato en el Registro de Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Fecha:** 2026-06-12  
**Estado:** Aceptada  
**Decisores:** ODIN (técnico), Jelkin (negocio), ZEUS (gobierno)  
**Consultores:** Equipo de seguridad y privacidad de Innovadataco

---

## 1. CONTEXT

El Proyecto 005 gestiona reportes de protección infantil. Los datos son altamente sensibles y los reportantes deben permanecer anónimos. Se requiere:

- Confidencialidad de la información en reposo.
- Anonimato del reportante (sin IP, user-agent, cookies ni metadata).
- Integridad de los datos (detección de manipulación).
- Disponibilidad básica protegida contra abuso (rate limiting).

---

## 2. DECISION

**Decidimos** usar **AES-256-GCM** con una **DEK aleatoria por campo** y una **KEK derivada de una variable de entorno** de 32 bytes, en lugar de encriptación determinista o claves únicas para toda la base de datos.

Cada campo sensible (`reported_identifier`, `description`, `evidence_content`) se encripta con una DEK única. La DEK se encripta con la KEK y se almacena junto al valor encriptado. El modelo `Report` no incluye columnas de metadata identificable. Se implementa rate limiting por IP con soporte opcional para Redis.

---

## 3. CONSEQUENCES

### 3.1 Positivas
- Cumplimiento con requisitos de anonimato.
- Encriptación autenticada que detecta tampering (GCM).
- Compromiso de una DEK no expone otros campos ni reportes.
- Escalabilidad del rate limiting mediante Redis.

### 3.2 Negativas
- No se puede buscar por contenido encriptado, solo por `report_hash`.
- La rotación de la KEK requiere re-encriptar todos los registros.
- El rate limiting en memoria no escala entre workers.

### 3.3 Neutras
- Esquema de base de datos simple (una tabla principal).
- API REST minimalista.

---

## 4. ALTERNATIVAS CONSIDERADAS

| Alternativa | Pros | Contras | Veredicto |
|-------------|------|---------|-----------|
| RSA | Bueno para intercambio de claves | Lento para datos de tamaño variable; más complejo | Rechazada |
| ChaCha20 | Rápido y seguro | No está de forma nativa en `cryptography` para este caso | Rechazada |
| AES-256-CBC | Ampliamente soportado | Sin autenticación; no detecta tampering | Rechazada |
| Encriptación determinista | Permite búsquedas | Vincula reportes; filtra información | Rechazada |
| **AES-256-GCM + DEK por campo** | Autenticado, flexible, seguro | No permite búsqueda por contenido | **Aceptada** |

---

## 5. IMPLEMENTATION

- Archivos modificados:
  - `src/backend/app/services/encryption.py`
  - `src/backend/app/models.py`
  - `src/backend/app/routers/reportes.py`
  - `src/backend/app/config.py`
  - `src/backend/app/services/rate_limit.py`
- Tests agregados:
  - `src/backend/tests/test_encryption.py`
  - `src/backend/tests/test_reportes.py`
  - `src/backend/tests/test_security.py`
- Fecha de implementación: 2026-06-12

---

## 6. NOTES

- Documentación complementaria: `security-checklist.md`, `spec.md`, `plan.md`.
- Revisión programada: antes del deploy a producción.
- La KEK debe generarse con: `openssl rand -hex 32`.

---

> Generado por ODIN — Innovadataco
