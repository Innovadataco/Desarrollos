# Tasks — SPEC-001: Registro Anónimo de Números Telefónicos

Origen: `specs/001-registro-anonimo/spec.md` y `specs/001-registro-anonimo/plan.md`.
Método: tests primero, implementación mínima, anonimato absoluto.

---

## Fase 1: Preparación del entorno

- [ ] **TASK-001: Crear estructura de carpetas del backend**
  - Crear `src/backend/app/`, `src/backend/app/routers/`, `src/backend/app/services/`, `src/backend/tests/`.
  - Crear archivos `__init__.py` vacíos donde apliquen.

- [ ] **TASK-002: Crear estructura de carpetas del frontend**
  - Crear `src/frontend/src/components/`.

- [ ] **TASK-003: Archivos de configuración base**
  - Crear `src/backend/requirements.txt` con FastAPI, SQLAlchemy, psycopg2-binary, cryptography, pydantic-settings, pytest, httpx.
  - Crear `src/frontend/package.json` con React 19, Vite, Tailwind CSS.
  - Actualizar `.env.example` con `DATABASE_URL` y `REPORT_ENCRYPTION_KEY`.

- [ ] **TASK-004: Configurar Docker Compose**
  - Crear/actualizar `docker-compose.yml` con servicios: `db` (PostgreSQL), `backend`, `frontend`.
  - Asegurar que el backend espere a la BD antes de iniciar.

---

## Fase 2: Backend — Modelo y base de datos

- [ ] **TASK-005: Implementar `database.py`**
  - Configurar engine, sessionmaker y `declarative_base()` con SQLAlchemy 2.0.
  - Soportar SQLite en memoria para tests mediante variable de entorno.

- [ ] **TASK-006: Implementar `models.py`**
  - Crear modelo `Report` con columnas: `id` (UUID PK), `report_hash`, `reported_identifier`, `description`, `evidence_type`, `evidence_content`, `reported_at`, `updated_at`.
  - Asegurar que no existen columnas de IP, user-agent ni metadata del dispositivo.

- [ ] **TASK-007: Implementar migración/esquema inicial**
  - Crear script `src/backend/alembic/` o usar `Base.metadata.create_all()` para el MVP.
  - Verificar que la tabla se crea correctamente en PostgreSQL.

---

## Fase 3: Backend — Encriptación

- [ ] **TASK-008: Implementar `services/encryption.py`**
  - Usar `cryptography` con AES-256-GCM.
  - Implementar generación de DEK por reporte.
  - Implementar encriptación de DEK con KEK derivada de `REPORT_ENCRYPTION_KEY`.
  - Funciones: `encrypt_field(plaintext, kek) -> bytes` y `decrypt_field(ciphertext, kek) -> str`.
  - Tests unitarios para encriptar/desencriptar y detectar tampering.

- [ ] **TASK-009: Implementar generación de `report_hash`**
  - Función determinista pero no reversible: `SHA-256(nonce + timestamp + normalized_identifier)`.
  - Garantizar unicidad; manejar colisiones con re-intento de nonce.

---

## Fase 4: Backend — API y validaciones

- [ ] **TASK-010: Implementar `schemas.py`**
  - Pydantic schemas para `ReportCreate`, `Evidence`, `ReportResponse`.
  - Validar longitudes y valores permitidos (`evidence_type` en `text`, `image`, `None`).

- [ ] **TASK-011: Implementar endpoint `POST /api/reportes`**
  - Recibir payload, encriptar campos sensibles, generar `report_hash`, guardar en BD.
  - Responder `201 Created` con `{ report_hash, reported_at }`.
  - No capturar ni almacenar IP, headers ni cookies del request.

- [ ] **TASK-012: Implementar rate limiting anónimo**
  - Middleware o dependency que limite a 5 peticiones por IP por hora.
  - Usar almacenamiento en memoria (o Redis si está disponible).
  - No persistir la IP más allá de la ventana de rate limit.

- [ ] **TASK-013: Implementar `GET /api/health`**
  - Responder `{ "status": "ok" }` y verificar conexión a BD opcionalmente.

- [ ] **TASK-014: Cablear `main.py`**
  - Incluir routers, excepciones y documentación OpenAPI automática.

---

## Fase 5: Backend — Tests

- [ ] **TASK-015: Configurar `tests/conftest.py`**
  - Fixture de base de datos SQLite en memoria.
  - Fixture de `TestClient`.
  - Fixture de clave de encriptación para tests.

- [ ] **TASK-016: Tests de creación de reporte**
  - Crear reporte válido con y sin evidencia.
  - Verificar respuesta `201` y presencia de `report_hash`.
  - Verificar que los datos se encriptan en BD (no están en texto plano).

- [ ] **TASK-017: Tests de validación**
  - Campos faltantes.
  - `evidence.type` inválido.
  - `evidence.content` faltante cuando `evidence.type` existe.

- [ ] **TASK-018: Tests de anonimato**
  - Verificar que no se guardan IPs, user-agents ni cookies.
  - Verificar que `report_hash` no se puede usar para rastrear al reportante.

- [ ] **TASK-019: Tests de rate limiting**
  - Enviar 6 reportes y verificar que el sexto devuelve `429`.
  - Verificar que no queda registro permanente de la IP.

- [ ] **TASK-020: Tests de encriptación**
  - Encriptar/desencriptar campo.
  - Detectar modificación del ciphertext.
  - Verificar que diferentes reportes generan DEKs distintas.

---

## Fase 6: Frontend

- [ ] **TASK-021: Implementar `ReportForm.jsx`**
  - Campos: identificador reportado, descripción, evidencia opcional (texto/imagen).
  - Validación básica en cliente.
  - Mensaje de confirmación con `report_hash` (sin vincular al reportante).

- [ ] **TASK-022: Implementar `App.jsx` y estilos**
  - Página simple con el formulario centrado, accesible desde móvil.
  - Tailwind CSS, sin tracking ni cookies.

- [ ] **TASK-023: Configurar PWA**
  - `vite-plugin-pwa` mínimo: manifest, íconos placeholder, service worker básico.
  - Asegurar que no se cachea información del reportante.

---

## Fase 7: Integración y validación

- [ ] **TASK-024: Levantar entorno completo con Docker Compose**
  - `docker compose up --build`.
  - Verificar que backend, frontend y base de datos se comunican.

- [ ] **TASK-025: Validar criterios de aceptación**
  - [ ] Formulario accesible desde móvil sin registro.
  - [ ] Reporte creado en BD encriptada.
  - [ ] No queda registro de IP, cookies ni metadata.
  - [ ] `report_hash` único y no rastreable.
  - [ ] Tests unitarios pasan al 100%.
  - [ ] Documentación OpenAPI generada y accesible en `/docs`.

- [ ] **TASK-026: Actualizar README.md del módulo**
  - Instrucciones de instalación, variables de entorno, cómo correr tests.

---

## Fase 8: Entrega

- [ ] **TASK-027: Revisión final y linting**
  - Ejecutar `ruff` / `black` en backend si aplica.
  - Ejecutar tests y asegurar cobertura ≥ 80%.

- [ ] **TASK-028: Crear PR**
  - Título sugerido: `Módulo Registro Anónimo - PROYECTO-005`.
  - Incluir resumen de cambios, tests ejecutados y decisión de encriptación.

---

## Notas

- Prioridad absoluta: anonimato. Si una tarea compromete el anonimato, se rechaza o se rediseña.
- No se guardan secrets en el repositorio; todas las claves van a `.env`.
- Cada decisión arquitectónica relevante debe reflejarse en un breve ADR si el proyecto lo requiere.
