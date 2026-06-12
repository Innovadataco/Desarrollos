# Plan Técnico — SPEC-001: Registro Anónimo de Números Telefónicos

## 1. Stack detallado

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| Frontend | React 19 + Vite + Tailwind CSS + PWA | Formulario ligero, accesible desde móvil, sin login, instalable como app. |
| Backend | Python 3.12 + FastAPI | Alto rendimiento, validación con Pydantic, OpenAPI automático. |
| ORM | SQLAlchemy 2.0 | Prevención de SQL Injection y modelado declarativo. |
| Base de datos | PostgreSQL 16 | Robustez, soporte nativo para UUID y JSONB. |
| Encriptación | `cryptography` (AES-256-GCM) | Encriptación autenticada de datos sensibles en reposo. |
| Rate limiting | `slowapi` o middleware propio con Redis | Mitiga spam sin persistir IPs. |
| Tests | `pytest` + `httpx.TestClient` | Tests unitarios y de integración para el endpoint. |
| Documentación API | OpenAPI/Swagger UI generada por FastAPI | Cumple criterio de aceptación de documentación API. |
| Contenedores | Docker + Docker Compose | Entorno reproducible para backend, frontend y base de datos. |

---

## 2. Modelo de datos

### Tabla: `reports`

| Columna | Tipo | Encriptada | Descripción |
|---------|------|------------|-------------|
| `id` | UUID PK | No | Identificador interno, no expuesto al reportante. |
| `report_hash` | VARCHAR(64), UNIQUE, INDEX | No | Hash único para seguimiento interno (`SHA-256` de nonce + timestamp + identificador normalizado). No vinculable al reportante. |
| `reported_identifier` | BYTEA | Sí | Número telefónico o usuario reportado. |
| `description` | BYTEA | Sí | Descripción del incidente. |
| `evidence_type` | VARCHAR(10) o NULL | No | Tipo de evidencia: `'text'` \| `'image'` \| `NULL`. |
| `evidence_content` | BYTEA o NULL | Sí | Evidencia en texto o imagen en base64. |
| `reported_at` | TIMESTAMP TZ | No | Fecha/hora automática del reporte. |
| `updated_at` | TIMESTAMP TZ | No | Última actualización. |

### Notas de diseño
- Ninguna columna almacena IP, user-agent, cookies ni metadata del dispositivo.
- `report_hash` se genera con un `nonce` aleatorio de 32 bytes; su propósito es solo evitar duplicados internos y permitir seguimiento administrativo sin identificar al reportante.
- Imágenes grandes: para producción se recomienda almacenarlas en un object storage (ej. MinIO/S3) y guardar en BD solo la referencia encriptada. Para este módulo se permite base64 si el tamaño es razonable (< 5 MB).

---

## 3. Endpoints API

### `POST /api/reportes`
Crea un reporte anónimo.

**Request body (JSON):**
```json
{
  "reported_identifier": "+573001234567",
  "description": "Recibí mensajes inapropiados de este número.",
  "evidence": {
    "type": "text",
    "content": "Captura de pantalla descriptiva..."
  }
}
```

**Validaciones:**
- `reported_identifier`: obligatorio, longitud máxima 255.
- `description`: obligatorio, longitud máxima 5000.
- `evidence.type`: opcional, solo `'text'` o `'image'`.
- `evidence.content`: opcional, obligatorio si `evidence.type` está presente.
- Rate limit: máximo 5 peticiones por IP por hora.

**Response 201 Created:**
```json
{
  "report_hash": "a1b2c3d4...",
  "reported_at": "2026-06-12T07:09:57Z"
}
```

**Response 429 Too Many Requests:**
```json
{
  "detail": "Has alcanzado el límite de reportes. Intenta más tarde."
}
```

### `GET /api/health`
Health check simple para monitoreo.

**Response 200 OK:**
```json
{
  "status": "ok"
}
```

---

## 4. Estrategia de encriptación

### Algoritmo
- **AES-256-GCM** mediante la librería `cryptography`.
- Ciphertext + nonce + tag almacenados juntos en la columna encriptada.

### Gestión de claves
- **KEK (Key Encryption Key):** clave maestra de 32 bytes derivada de `REPORT_ENCRYPTION_KEY` (variable de entorno, nunca en código).
- **DEK (Data Encryption Key):** por cada reporte se genera una DEK aleatoria de 32 bytes.
- La DEK se encripta con la KEK y se almacena junto al reporte.
- Ventaja: rotación de claves maestras sin re-encriptar todos los datos; basta con re-encriptar las DEKs.

### Campos encriptados
- `reported_identifier`
- `description`
- `evidence_content`

### Campos NO encriptados
- `id`, `report_hash`, `evidence_type`, `reported_at`, `updated_at`

### Consideraciones de seguridad
- La KEK debe cargarse desde un gestor de secretos en producción (HashiCorp Vault, AWS KMS, etc.) o desde `.env` en desarrollo.
- Nunca se registran ni almacenan datos de identificación del reportante.

---

## 5. Estructura de carpetas

```
specs/001-registro-anonimo/
├── spec.md
├── plan.md          # este archivo
└── tasks.md         # tareas derivadas (siguiente paso)

src/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Punto de entrada FastAPI
│   │   ├── config.py            # Configuración y variables de entorno
│   │   ├── database.py          # Sesión y engine de SQLAlchemy
│   │   ├── models.py            # Modelo Report
│   │   ├── schemas.py           # Esquemas Pydantic
│   │   ├── dependencies.py      # Dependencias FastAPI (DB, rate limit)
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── reportes.py      # Endpoint POST /api/reportes
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── encryption.py    # Lógica AES-256-GCM + DEK/KEK
│   │       └── rate_limit.py    # Rate limiting por IP sin persistencia
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Fixtures (DB en memoria, cliente)
│   │   └── test_reportes.py     # Tests del endpoint
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ReportForm.jsx   # Formulario anónimo
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 6. Decisiones arquitectónicas clave

1. **Anonimato absoluto:** no se guarda IP, user-agent, cookies ni metadata. El rate limit usa la IP solo en memoria durante la ventana de tiempo.
2. **Encriptación selectiva:** solo datos sensibles se encriptan; metadatos operativos (`report_hash`, timestamps) permanecen en claro para consultas internas.
3. **DEK por reporte:** mejora la seguridad a largo plazo y facilita la rotación de claves maestras.
4. **Sin autenticación:** el formulario es público y no requiere login, reduciendo la fricción para el reportante.
5. **OpenAPI automática:** FastAPI genera la documentación sin esfuerzo adicional.

---

## 7. Próximos pasos

1. Generar `tasks.md` con las tareas implementables.
2. Implementar backend (modelo, encriptación, endpoint, tests).
3. Implementar frontend (formulario anónimo).
4. Levantar entorno con Docker Compose.
5. Ejecutar tests y validar criterios de aceptación.
