# SPEC-005 — Panel de Administración (Módulo 005)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ NUEVO — Pendiente desarrollo

---

## 1. RESUMEN

El Módulo 005 implementa el panel de administración para operadores autorizados de Innovadataco o autoridades contratantes. Permite: autenticación segura, visualización de reportes con filtros, desencriptación bajo demanda con audit trail, cambio de estado de reportes, y export de datos para autoridades.

**Solo personal autorizado puede acceder.** Todo acceso a datos sensibles se registra en audit trail.

---

## 2. FLUJO DE ADMIN

```
[Login]
   │
   ├── Username + Password (bcrypt)
   ├── JWT token (expira 1h, refresh 24h)
   └── 2FA opcional (TOTP, configurado por admin root)
   │
   ▼
[Dashboard]
   │
   ├── Métricas: reportes hoy, semana, mes
   ├── Semáforo global: verde/amarillo/rojo/negro distribución
   └── Alertas: reportes critical/sin revisar
   │
   ▼
[Lista de Reportes]
   │
   ├── Filtros: fecha, score, nivel, categoría, estado, ciudad
   ├── Paginación: 20 por página
   └── Acciones: ver, desencriptar, cambiar estado, exportar
   │
   ▼
[Detalle de Reporte]
   │
   ├── Metadata: hash, fecha, categoría, score, nivel
   ├── Contenido: [BOTÓN "Desencriptar"] → audit trail
   │   ├── Identificador reportado
   │   ├── Descripción del incidente
   │   └── Evidencia multimedia (thumbnail + descargar)
   └── Cambio de estado: Nuevo → En revisión → Escalado → Cerrado
   │
   ▼
[Perfil de Identificador]
   │
   ├── Módulo 004: timeline, ciudades, score, red organizada
   └── Exportar perfil: JSON/PDF
   │
   ▼
[Export]
   │
   ├── JSON: estructurado, schema fijo
   └── PDF: branding Innovadataco, formato institucional
```

---

## 3. ENDPOINTS

### Auth

#### `POST /api/auth/login`
```json
{
  "username": "admin",
  "password": "..."
}
```
Response 200:
```json
{
  "access_token": "jwt-1h",
  "refresh_token": "jwt-24h",
  "token_type": "bearer"
}
```

#### `POST /api/auth/refresh`

#### `POST /api/auth/2fa/setup` (solo admin root)

#### `POST /api/auth/2fa/verify`

### Reportes

#### `GET /api/admin/reports`
Query params: `date_from`, `date_to`, `score_min`, `level`, `category`, `status`, `city`, `page`, `limit`

Response 200:
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "reports": [
    {
      "id": "uuid",
      "report_hash": "SHA256-64CHAR",
      "reported_at": "2026-06-13T10:00:00Z",
      "score": 0.87,
      "level": "severe",
      "category": "grooming",
      "status": "nuevo",
      "city": "Bogotá",
      "country": "Colombia",
      "evidence_type": "image",
      "has_evidence": true
    }
  ]
}
```

#### `GET /api/admin/reports/{report_id}`

Metadata sin desencriptar. Botón para desencriptar.

#### `POST /api/admin/reports/{report_id}/decrypt`

**Body:** `{"reason": "Revisión de reporte critical"}`

Response 200:
```json
{
  "decrypted_at": "2026-06-13T11:30:00Z",
  "reported_identifier": "+573001234567",
  "description": "Texto del reporte...",
  "evidence_url": "https://cdn.semaforo.com/enc/abc123?token=temp",
  "evidence_type": "image",
  "audit_log_id": "uuid"
}
```

**Restricciones:**
- Solo admins con rol `reviewer` o `supervisor` pueden desencriptar
- Max 10 desencriptaciones por hora por admin
- Evidence URL expira en 5 minutos
- Audit trail obligatorio

#### `PATCH /api/admin/reports/{report_id}/status`

```json
{
  "status": "en_revision",
  "notes": "Iniciando revisión del reporte"
}
```

Estados válidos: `nuevo`, `en_revision`, `escalado`, `cerrado`

### Dashboard

#### `GET /api/admin/dashboard`
Response 200:
```json
{
  "today": {"reports": 5, "critical": 1, "high": 2},
  "week": {"reports": 23, "by_day": [3,4,5,2,4,3,2]},
  "month": {"reports": 87, "trend": "+12%"},
  "semaforo": {"verde": 45, "amarillo": 23, "rojo": 15, "negro": 4},
  "pending_review": 8,
  "networks_detected": 2
}
```

### Export

#### `POST /api/admin/export`
```json
{
  "format": "json", // o "pdf"
  "filters": {"date_from": "2026-06-01", "level": "critical"},
  "include_decrypted": false
}
```

---

## 4. MODELO DE ROLES

| Rol | Permisos | Descripción |
|-----|----------|-------------|
| `viewer` | Ver reportes, dashboard, perfiles | Solo lectura, no desencripta |
| `reviewer` | Viewer + desencriptar + cambiar estado | Revisión operativa |
| `supervisor` | Reviewer + export + configurar umbrales | Gestión de alertas |
| `admin` | Supervisor + gestionar usuarios + 2FA | Administración |
| `root` | Todo + rotar claves de encriptación | Técnico, Innovadataco |

---

## 5. AUDIT TRAIL

Cada acción sensible se registra en `AuditLog`:

| Campo | Descripción |
|-------|-------------|
| `admin_id` | Quién hizo la acción |
| `action` | login, view, decrypt, status_change, export, delete |
| `report_id` | FK (nullable) |
| `profile_id` | FK (nullable) |
| `details` | JSON con metadata de la acción |
| `ip_address` | IP del admin (no del reportante) |
| `user_agent` | Browser del admin |
| `timestamp` | Fecha/hora exacta |

**Acciones auditadas:**
- Login/logout
- Desencriptación de reporte (con razón)
- Cambio de estado de reporte
- Export de datos
- Visualización de perfil de identificador
- Configuración de umbrales de alerta

---

## 6. DESECRIPTACIÓN BAJO DEMANDA

```
Admin solicita desencriptar
        │
        ▼
[Validar permisos (rol >= reviewer)]
        │
        ▼
[Validar límite: 10 desencriptaciones/hora/admin]
        │
        ▼
[Pedir razón (mínimo 20 caracteres)]
        │
        ▼
[Desencriptar en memoria (nunca en disco)]
        │
        ▼
[Retornar texto + evidence URL temporal (5 min)]
        │
        ▼
[Registrar en AuditLog]
        │
        ▼
[Evidence URL expira en 5 min]
```

---

## 7. CRITERIOS DE ACEPTACIÓN (DoD)

- [ ] Auth con JWT funcional (login, refresh, 2FA opcional)
- [ ] Dashboard muestra métricas en tiempo real
- [ ] Lista de reportes con filtros y paginación
- [ ] Desencriptación bajo demanda con audit trail
- [ ] Límite de 10 desencriptaciones/hora por admin
- [ ] Evidence URL expira en 5 minutos
- [ ] Cambio de estado funciona (Nuevo → En revisión → Escalado → Cerrado)
- [ ] Export JSON y PDF genera archivos correctos
- [ ] Roles funcionan (viewer, reviewer, supervisor, admin, root)
- [ ] No desencripta sin razón (mínimo 20 caracteres)
- [ ] No desencripta viewer (solo reviewer+)
- [ ] Tests E2E con Playwright (flujo completo admin)
- [ ] Tests unitarios ≥ 80% cobertura
- [ ] ADR aprobado (auth + audit trail)

---

> *SPEC generado por ZEUS — Innovadataco*  
> *Módulo 005 — Nuevo en v2.0*
