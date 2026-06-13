# SPEC-006 — Pasarela Institucional (Módulo 006)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ NUEVO — Pendiente desarrollo

---

## 1. RESUMEN

El Módulo 006 implementa la pasarela institucional: API gateway para integración con autoridades colombianas (ICBF, Fiscalía, Policía, Te Protejo) y estándares internacionales (NCMEC). Permite enviar alertas estructuradas, resúmenes periódicos, y reportes en formatos estándar, sin exponer identidad del reportante ni datos sin autorización.

**Innovadataco es canal tecnológico.** No investiga, no juzga, no alerta al agresor. La investigación judicial es responsabilidad exclusiva de las autoridades.

---

## 2. INTEGRACIONES SOPORTADAS

| Institución | Sistema | Método | Estado |
|-------------|---------|--------|--------|
| ICBF | Línea 141 / Te Protejo | Email + API webhook (si disponible) | Planificado |
| Fiscalía General | Unidad de Delitos Sexuales | Email estructurado + portal web | Planificado |
| Policía Nacional | GAULA / Grupo Infancia | Email + API (si disponible) | Planificado |
| NCMEC | CyberTipline | API estándar NCMEC | Planificado |
| Interpol | Crimes Against Children | Email (internacional) | Futuro |

---

## 3. ALERTAS AUTOMÁTICAS

### 3.1 Umbrales de Alerta (configurables por admin)

| Nivel | Score | Tiempo de envío | Destinatarios |
|-------|-------|-----------------|---------------|
| Severe | ≥ 0.85 | Inmediato (< 15 min) | ICBF + Fiscalía (critical) |
| Critical | 0.70 - 0.85 | < 4 horas | ICBF (high) |
| High | 0.50 - 0.70 | < 24 horas | ICBF (daily digest) |
| Medium | 0.30 - 0.50 | Resumen semanal | ICBF (weekly digest) |
| Low | < 0.30 | Resumen mensual | Panel admin solo (no autoridades) |

### 3.2 Detección de Red Organizada (⚫ NEGRO)

- **Siempre inmediato:** Sin importar score individual, si `is_network = true`
- **Destinatarios:** ICBF + Fiscalía + Policía (todos)
- **Contenido:** Perfil completo del identificador (agregado, no individual)
- **Prioridad:** Máxima

---

## 4. FORMATOS DE EXPORTACIÓN

### 4.1 JSON Estructurado (estándar interno)

```json
{
  "report_id": "uuid",
  "report_hash": "SHA256-64CHAR",
  "reported_at": "2026-06-13T10:00:00Z",
  "category": "grooming",
  "score": 0.87,
  "level": "severe",
  "identifier_type": "phone",
  "identifier_normalized": "+573001234567",
  "identifier_hash": "SHA256-IDENTIFIER",
  "city": "Bogotá",
  "country": "Colombia",
  "evidence_types": ["image", "screenshot"],
  "description_summary": "Resumen automatizado de 200 caracteres (no texto original)",
  "analysis": {
    "model_version": "grooming-v1.0",
    "grooming_indicators": ["secrecion", "aislamiento"],
    "confidence": 0.92
  },
  "profile": {
    "report_count": 7,
    "score_average": 0.78,
    "is_network": false,
    "cities_count": 1,
    "countries_count": 1
  }
}
```

**Nota:** El texto original del reporte NUNCA se incluye. Solo resumen automatizado de 200 caracteres generado por el modelo NLP.

### 4.2 PDF Institucional (branding Innovadataco)

- Portada con logo, fecha, número de reporte
- Resumen ejecutivo (1 página)
- Detalle del reporte (sin identificar al reportante)
- Análisis de IA (score, categoría, indicadores)
- Perfil del identificador (si aplica)
- Evidencia: thumbnails con marca de agua (sin texto identificable)
- Pie de página: "Este documento es una alerta comunitaria generada por el Semáforo de Confianza de Innovadataco. La investigación judicial es responsabilidad exclusiva de las autoridades competentes."

### 4.3 NCMEC Format (CyberTipline)

Conforme al estándar NCMEC para reportes internacionales de explotación infantil.

---

## 5. ENDPOINTS

### 5.1 Internos (Panel Admin)

#### `POST /api/admin/alerts/send`

Enviar alerta manual por reporte.

```json
{
  "report_id": "uuid",
  "destinations": ["icbf", "fiscalia"],
  "format": "json", // o "pdf"
  "include_profile": true,
  "notes": "Reporte severe, grooming detectado."
}
```

#### `POST /api/admin/digest/generate`

Generar resumen periódico.

```json
{
  "period": "daily", // daily, weekly, monthly
  "date": "2026-06-13",
  "format": "json",
  "min_level": "high"
}
```

#### `GET /api/admin/alerts/status/{alert_id}`

Estado de envío de alerta.

```json
{
  "alert_id": "uuid",
  "status": "delivered", // pending, delivered, failed, retrying
  "destination": "icbf",
  "sent_at": "2026-06-13T10:15:00Z",
  "delivered_at": "2026-06-13T10:16:00Z",
  "retries": 0,
  "error": null
}
```

### 5.2 Externos (API Gateway para Autoridades)

#### `POST /api/gateway/v1/reports` (ICBF/Fiscalía/Policía)

**API key requerida.** Autenticación por API key institucional.

```json
{
  "api_key": "institution_key",
  "report_hash": "SHA256-64CHAR",
  "request_type": "full" // o "summary"
}
```

Response 200:
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

**Restricciones:**
- Solo instituciones con API key válida y contrato firmado
- Rate limit: 100 requests/hour por institución
- No retorna identificador real (solo hash y tipo)
- No retorna texto original del reporte

#### `POST /api/gateway/v1/digest` (Resumen periódico)

```json
{
  "api_key": "institution_key",
  "period": "daily",
  "date": "2026-06-13"
}
```

#### `POST /api/gateway/v1/confirm` (Confirmación de recepción)

```json
{
  "api_key": "institution_key",
  "report_hash": "SHA256-64CHAR",
  "status": "received", // received, in_review, investigating, closed
  "notes": "Caso asignado a investigador #1234"
}
```

---

## 6. CONFIGURACIÓN DE ALERTAS

### Panel Admin (Supervisor+)

| Configuración | Valor Default | Rango |
|---------------|---------------|-------|
| Umbral severe | 0.85 | 0.7 - 1.0 |
| Umbral critical | 0.70 | 0.5 - 0.85 |
| Umbral high | 0.50 | 0.3 - 0.7 |
| Umbral medium | 0.30 | 0.1 - 0.5 |
| Alerta severe: inmediato | true | boolean |
| Alerta critical: 4h | true | boolean |
| Alerta high: 24h | true | boolean |
| Alerta medium: weekly | true | boolean |
| Alerta red organizada: inmediato | true | boolean (no editable) |
| Destinatarios severe | ICBF + Fiscalía | multi-select |
| Destinatarios critical | ICBF | multi-select |
| Destinatarios high | ICBF | multi-select |
| Destinatarios medium | — | multi-select |
| Formato default | JSON | JSON / PDF |
| Incluir perfil | true | boolean |
| Incluir resumen IA | true | boolean |

---

## 7. MODELO DE DATOS

### Entidad `Alert`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| report_id | UUID | FK → Report |
| destination | String(50) | icbf, fiscalia, policia, ncmec |
| format | String(20) | json, pdf, ncmec |
| status | String(20) | pending, delivered, failed, retrying |
| sent_at | DateTime | Cuándo se envió |
| delivered_at | DateTime | Cuándo se confirmó entrega |
| retries | Integer | Intentos de reenvío |
| error | Text | Error si falló |
| created_at | DateTime | Timestamp |

### Entidad `Digest`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| period | String(20) | daily, weekly, monthly |
| date | Date | Fecha del digest |
| destination | String(50) | Institución |
| report_count | Integer | Reportes incluidos |
| severe_count | Integer | Reportes severe |
| critical_count | Integer | Reportes critical |
| high_count | Integer | Reportes high |
| content | JSON | Contenido del digest |
| sent_at | DateTime | Cuándo se envió |
| status | String(20) | pending, delivered, failed |

### Entidad `Institution`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| name | String(100) | Nombre de la institución |
| code | String(20) | Código: icbf, fiscalia, policia, ncmec |
| api_key | String(64) | API key para gateway (bcrypt) |
| contact_email | String(255) | Email para alertas |
| contact_phone | String(20) | Teléfono para alertas críticas |
| contract_active | Boolean | ¿Tiene contrato firmado? |
| contract_expires | Date | Fecha de expiración del contrato |
| alert_config | JSON | Configuración de alertas específica |
| created_at | DateTime | Timestamp |

---

## 8. CRITERIOS DE ACEPTACIÓN (DoD)

- [ ] Endpoint POST /api/admin/alerts/send funcional (manual)
- [ ] Alertas automáticas por severidad funcionan (cron job)
- [ ] Alerta severe enviada en < 15 min desde recepción del reporte
- [ ] Alerta red organizada enviada inmediatamente (sin importar score)
- [ ] Digest diario, semanal, mensual generado y enviado correctamente
- [ ] API Gateway funcional con API key (autenticación institucional)
- [ ] API Gateway no retorna datos identificables del reportante
- [ ] API Gateway no retorna texto original del reporte
- [ ] Rate limiting de 100 req/hr por institución
- [ ] Confirmación de recepción por institución (POST /api/gateway/v1/confirm)
- [ ] Formatos JSON, PDF, y NCMEC generados correctamente
- [ ] Resumen de IA de 200 caracteres generado automáticamente
- [ ] Panel admin permite configurar umbrales y destinatarios
- [ ] Tests de integración con mock servers (pytest)
- [ ] Tests E2E con Playwright (panel admin: configuración de alertas)
- [ ] Tests unitarios ≥ 80% cobertura
- [ ] ADR-005 aprobado (integración con autoridades)

---

> *SPEC generado por ZEUS — Innovadataco*  
> *Módulo 006 — Nuevo en v2.0*
