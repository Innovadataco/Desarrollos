# API Reference — Semáforo de Confianza

**Proyecto:** Semáforo de Confianza (005)  
**Base URL:** `https://api.semaforo.innovadataco.com`  
**Versión API:** `v1`  
**Fecha:** 13 de junio 2026  

---

## Autenticación

### Pública (sin auth)
- `POST /api/v1/reportes` — Reporte anónimo
- `GET /api/v1/validate/{identifier}` — Consulta semáforo
- `GET /api/v1/health` — Health check

### Admin (JWT Bearer)
- `Authorization: Bearer <jwt_token>`
- Todos los endpoints `/api/v1/admin/*`
- Roles: `viewer`, `reviewer`, `supervisor`, `admin`, `root`

### Institucional (API Key)
- `X-API-Key: <institution_api_key>`
- Todos los endpoints `/api/v1/gateway/*`
- Rate limit: 100 requests/hour

---

## Endpoints Públicos

### `POST /api/v1/reportes` — Crear Reporte Anónimo

**Headers:**
```
Content-Type: application/json
X-No-Track: 1
```

**Body:**
```json
{
  "reported_identifier": "+573001234567",
  "description": "Este número contactó a mi hija de 12 años por WhatsApp pidiendo fotos. Se hace pasar por compañero de colegio.",
  "category": "grooming",
  "evidence_type": "image",
  "evidence_content": "base64_encoded_encrypted_image...",
  "evidence_media_url": "https://cdn.semaforo.com/enc/abc123",
  "consent_location": true
}
```

**Response 201 Created:**
```json
{
  "report_hash": "SHA256-64CHAR",
  "message": "Reporte recibido. Guarde este código como único recibo.",
  "warning": "No podemos contactarlo. No guardamos ningún dato de identificación."
}
```

**Response 429 Too Many Requests:**
```json
{
  "error": "Demasiados reportes desde esta conexión. Espere 1 hora.",
  "retry_after": 3600
}
```

**Rate Limit:** 5/hour por IP (hashed)

---

### `GET /api/v1/validate/{identifier}` — Consultar Semáforo

**Parámetros:**
```
identifier: string (teléfono, email, @usuario, URL)
```

**Response 200 — Sin reportes (🟢 VERDE):**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "semaforo": "verde",
  "report_count": 0,
  "score_average": null,
  "score_max": null,
  "first_reported_at": null,
  "last_reported_at": null,
  "message": "Sin reportes registrados. El semáforo está verde.",
  "report_button": true
}
```

**Response 200 — Con reportes (🔴 ROJO):**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "semaforo": "rojo",
  "report_count": 7,
  "score_average": 0.78,
  "score_max": 0.95,
  "first_reported_at": "2026-04-15",
  "last_reported_at": "2026-06-10",
  "categories": ["grooming", "solicitud_material"],
  "cities_count": 4,
  "countries_count": 2,
  "is_network": true,
  "message": "Este identificador tiene 7 reportes de contacto inapropiado con menores, detectado desde 4 ciudades y 2 países. Posible red organizada.",
  "report_button": true
}
```

**Response 429 Too Many Requests:**
```json
{
  "error": "Demasiadas consultas. Espere 1 hora.",
  "retry_after": 3600
}
```

**Rate Limit:** 10/hour por IP (hashed)

---

### `GET /api/v1/health` — Health Check

**Response 200:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-06-13T10:00:00Z",
  "services": {
    "database": "ok",
    "redis": "ok",
    "encryption": "ok"
  }
}
```

---

## Endpoints Admin (JWT)

### Auth

#### `POST /api/v1/admin/auth/login`

**Body:**
```json
{
  "username": "admin",
  "password": "..."
}
```

**Response 200:**
```json
{
  "access_token": "jwt-1h",
  "token_type": "bearer"
}
```

> Nota: el backend emite un único token de acceso JWT. El refresh token está planificado para futuras versiones.

---

### Dashboard

#### `GET /api/v1/admin/dashboard`

**Response 200:**
```json
{
  "today": {"reports": 5, "critical": 1, "high": 2},
  "week": {"reports": 23, "by_day": [3, 4, 5, 2, 4, 3, 2]},
  "month": {"reports": 87, "trend": "+12%"},
  "semaforo": {"verde": 45, "amarillo": 23, "rojo": 15, "negro": 4},
  "pending_review": 8,
  "networks_detected": 2,
  "alerts_sent_today": 3
}
```

---

### Reportes

#### `GET /api/v1/admin/reports`

**Query Parameters:**
```
?date_from=2026-06-01&date_to=2026-06-30
&score_min=0.5&level=critical
&category=grooming&status=nuevo
&city=Bogotá&country=Colombia
&page=1&limit=20
```

**Response 200:**
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

#### `GET /api/v1/admin/reports/{report_id}`

**Response 200:**
```json
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
  "has_evidence": true,
  "can_decrypt": true
}
```

#### `POST /api/v1/admin/reports/{report_id}/decrypt`

**Body:**
```json
{
  "reason": "Revisión de reporte severe, grooming detectado. Iniciando investigación preliminar."
}
```

**Restricciones:**
- Razón mínimo 20 caracteres
- Máximo 10 desencriptaciones/hora por admin
- Solo roles `reviewer`, `supervisor`, `admin`, `root`

**Response 200:**
```json
{
  "decrypted_at": "2026-06-13T11:30:00Z",
  "reported_identifier": "+573001234567",
  "description": "Este número contactó a mi hija...",
  "evidence_url": "https://cdn.semaforo.com/enc/abc123?token=temp-jwt-5min",
  "evidence_type": "image",
  "audit_log_id": "uuid"
}
```

#### `PATCH /api/v1/admin/reports/{report_id}/status`

**Body:**
```json
{
  "status": "en_revision",
  "notes": "Iniciando revisión del reporte severe"
}
```

**Estados válidos:** `nuevo`, `en_revision`, `escalado`, `cerrado`

**Response 200:**
```json
{
  "id": "uuid",
  "status": "en_revision",
  "previous_status": "nuevo",
  "changed_at": "2026-06-13T11:30:00Z",
  "changed_by": "admin_username"
}
```

---

### Perfiles

#### `GET /api/v1/admin/profiles`

Lista todos los perfiles con filtros opcionales.

**Query Parameters:**
```
?report_count_min=3&score_min=0.5&is_network=true
```

**Response 200:**
```json
[
  {
    "identifier_hash": "SHA256-DE-IDENTIFICADOR",
    "identifier_type": "phone",
    "report_count": 12,
    "score_average": 0.74,
    "score_max": 0.95,
    "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
    "countries": ["Colombia", "México"],
    "cities_count": 4,
    "countries_count": 2,
    "is_network": true,
    "evidence_types": ["image", "audio", "screenshot"],
    "categories": ["grooming", "solicitud_material", "cita_persona"],
    "first_reported": "2026-02-15",
    "last_reported": "2026-06-10",
    "timeline": [
      {"month": "2026-02", "count": 2, "score_avg": 0.65},
      {"month": "2026-03", "count": 3, "score_avg": 0.72}
    ],
    "alert": "POSIBLE RED ORGANIZADA: 12 reportes desde 4 ciudades y 2 países."
  }
]
```

#### `GET /api/v1/admin/profiles/{identifier_hash}`

**Response 200:**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "identifier_type": "phone",
  "report_count": 12,
  "score_average": 0.74,
  "score_max": 0.95,
  "score_min": 0.45,
  "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
  "countries": ["Colombia", "México"],
  "cities_count": 4,
  "countries_count": 2,
  "is_network": true,
  "evidence_types": ["image", "audio", "screenshot"],
  "categories": ["grooming", "solicitud_material", "cita_persona"],
  "first_reported": "2026-02-15",
  "last_reported": "2026-06-10",
  "timeline": [
    {"month": "2026-02", "count": 2, "score_avg": 0.65},
    {"month": "2026-03", "count": 3, "score_avg": 0.72},
    {"month": "2026-04", "count": 4, "score_avg": 0.78},
    {"month": "2026-05", "count": 2, "score_avg": 0.81},
    {"month": "2026-06", "count": 1, "score_avg": 0.85}
  ],
  "alert": "POSIBLE RED ORGANIZADA: 12 reportes desde 4 ciudades y 2 países."
}
```

#### `GET /api/v1/admin/profiles/{identifier_hash}/timeline`

**Response 200:**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "timeline": [
    {"month": "2026-02", "count": 2, "score_avg": 0.65}
  ]
}
```

#### `GET /api/v1/admin/profiles/{identifier_hash}/updates`

Audit trail de cambios en el perfil.

**Response 200:**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "updates": [
    {
      "id": "uuid",
      "old_score_avg": 0.65,
      "new_score_avg": 0.74,
      "old_cities_count": 2,
      "new_cities_count": 4,
      "old_countries_count": 1,
      "new_countries_count": 2,
      "old_is_network": false,
      "new_is_network": true,
      "triggered_network": true,
      "created_at": "2026-06-10T12:00:00Z"
    }
  ]
}
```

#### `GET /api/v1/admin/profiles/networks/list`

Lista todos los identificadores con `is_network = true`.

**Response 200:**
```json
[
  {
    "identifier_hash": "SHA256-1",
    "identifier_type": "phone",
    "report_count": 12,
    "cities_count": 4,
    "countries_count": 2,
    "score_max": 0.95,
    "first_reported": "2026-02-15",
    "last_reported": "2026-06-10",
    "is_network": true,
    "alert": "POSIBLE RED ORGANIZADA: 12 reportes desde 4 ciudades y 2 países."
  }
]
```

---

### Alertas y Export

#### `POST /api/v1/admin/alerts/send`

**Body:**
```json
{
  "report_id": "uuid",
  "destinations": ["icbf", "fiscalia"],
  "format": "json",
  "include_profile": true,
  "notes": "Reporte severe, grooming detectado."
}
```

**Response 202:**
```json
{
  "alert_id": "uuid",
  "status": "pending",
  "destinations": ["icbf", "fiscalia"],
  "estimated_delivery": "2026-06-13T10:15:00Z"
}
```

#### `GET /api/v1/admin/alerts/{alert_id}/status`

**Response 200:**
```json
{
  "alert_id": "uuid",
  "status": "delivered",
  "destination": "icbf",
  "sent_at": "2026-06-13T10:15:00Z",
  "delivered_at": "2026-06-13T10:16:00Z",
  "retries": 0,
  "error": null
}
```

#### `POST /api/v1/admin/export`

**Body:**
```json
{
  "format": "json",
  "filters": {
    "date_from": "2026-06-01",
    "date_to": "2026-06-30",
    "level": "critical"
  },
  "include_decrypted": false
}
```

**Response 202:**
```json
{
  "export_id": "uuid",
  "status": "processing",
  "estimated_completion": "2026-06-13T10:05:00Z",
  "download_url": "https://api.semaforo.innovadataco.com/api/v1/admin/export/uuid/download"
}
```

---

### Audit Trail

#### `GET /api/v1/admin/audit`

**Query Parameters:**
```
?user_id=uuid&action=decrypt&report_id=uuid&page=1&limit=50
```

**Response 200:**
```json
{
  "total": 150,
  "page": 1,
  "limit": 50,
  "logs": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "username": "admin",
      "action": "decrypt",
      "report_id": "uuid",
      "details": {
        "reason": "Revisión de reporte severe..."
      },
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "created_at": "2026-06-13T11:30:00Z"
    }
  ]
}
```

---

### Configuración

#### `GET /api/v1/admin/config`

**Response 200:**
```json
{
  "threshold_severe": 0.85,
  "threshold_critical": 0.70,
  "threshold_high": 0.50,
  "threshold_medium": 0.30,
  "alert_severe_immediate": true,
  "alert_critical_4h": true,
  "alert_high_24h": true,
  "alert_medium_weekly": true,
  "alert_network_immediate": true,
  "digest_daily_time": "08:00",
  "digest_weekly_day": 1,
  "digest_weekly_time": "08:00"
}
```

#### `PATCH /api/v1/admin/config`

**Body:**
```json
{
  "threshold_severe": 0.80,
  "alert_critical_4h": false
}
```

**Restricción:** Solo `supervisor`, `admin`, `root`

---

### Usuarios (Admin Only)

#### `GET /api/v1/admin/users`

#### `POST /api/v1/admin/users`

**Body:**
```json
{
  "username": "new_reviewer",
  "password": "secure_password_123",
  "role": "reviewer",
  "email": "reviewer@innovadataco.com"
}
```

#### `PATCH /api/v1/admin/users/{user_id}`

#### `DELETE /api/v1/admin/users/{user_id}`

---

## Endpoints Gateway (Institucional — API Key)

#### `POST /api/v1/gateway/reports`

**Headers:**
```
X-API-Key: institution_api_key
Content-Type: application/json
```

**Body:**
```json
{
  "report_hash": "SHA256-64CHAR",
  "request_type": "full"
}
```

**Response 200:**
```json
{
  "report_hash": "SHA256-64CHAR",
  "category": "grooming",
  "score": 0.87,
  "level": "severe",
  "reported_at": "2026-06-13T10:00:00Z",
  "city": "Bogotá",
  "country": "Colombia",
  "evidence_types": ["image"],
  "description_summary": "Resumen de 200 chars...",
  "analysis": {
    "grooming_indicators": ["secrecion", "aislamiento"],
    "confidence": 0.92
  },
  "profile": {
    "report_count": 7,
    "score_average": 0.78,
    "is_network": false
  }
}
```

**Rate Limit:** 100/hour por API key

---

#### `POST /api/v1/gateway/digest`

**Body:**
```json
{
  "period": "daily",
  "date": "2026-06-13"
}
```

**Response 200:**
```json
{
  "period": "daily",
  "date": "2026-06-13",
  "report_count": 5,
  "severe_count": 1,
  "critical_count": 2,
  "high_count": 1,
  "medium_count": 1,
  "network_count": 0,
  "reports": [
    {
      "report_hash": "SHA256",
      "category": "grooming",
      "score": 0.87,
      "level": "severe",
      "city": "Bogotá",
      "description_summary": "Resumen..."
    }
  ]
}
```

---

#### `POST /api/v1/gateway/confirm`

**Body:**
```json
{
  "report_hash": "SHA256-64CHAR",
  "status": "received",
  "notes": "Caso asignado a investigador #1234"
}
```

**Response 200:**
```json
{
  "confirmed": true,
  "report_hash": "SHA256-64CHAR",
  "status": "received",
  "confirmed_at": "2026-06-13T10:20:00Z"
}
```

---

## Códigos de Error

| Código | Descripción | Acción |
|--------|-------------|--------|
| `400` | Bad Request | Revisar body del request |
| `401` | Unauthorized | Verificar JWT o API key |
| `403` | Forbidden | Sin permisos para esta acción |
| `404` | Not Found | Recurso no existe |
| `429` | Too Many Requests | Rate limit excedido, esperar retry_after |
| `500` | Internal Server Error | Contactar soporte |
| `503` | Service Unavailable | Mantenimiento o fallo de servicio |

---

## Rate Limits

| Endpoint | Límite | Ventana |
|----------|--------|---------|
| `POST /api/v1/reportes` | 5 | 1 hora por IP |
| `GET /api/v1/validate/{id}` | 10 | 1 hora por IP |
| `GET /api/v1/health` | 100 | 1 hora por IP |
| `POST /api/v1/admin/auth/login` | 5 | 15 min por IP |
| `POST /api/v1/admin/reports/{id}/decrypt` | 10 | 1 hora por admin |
| `POST /api/v1/gateway/*` | 100 | 1 hora por API key |
| `GET /api/v1/admin/*` | 1000 | 1 hora por admin |

---

> *Documento generado por ZEUS — Innovadataco*  
> *API v1.0 — Semáforo de Confianza*
