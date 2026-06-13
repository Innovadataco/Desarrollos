# Protección Infantil Comunitaria

Sistema de reporte anónimo y seguro para incidentes de protección infantil.

## Stack

- **Frontend:** React 19 + Vite + Tailwind CSS
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL/SQLite
- **Encriptación:** AES-256-GCM (DEK por campo, KEK derivada)
- **Rate Limiting:** Redis (prod) / Memoria (dev)
- **CI/CD:** GitHub Actions
- **Contenedores:** Docker + Docker Compose

## Variables de Entorno

Copiar `src/backend/.env.example` a `src/backend/.env` y configurar:

- `DATABASE_URL` — URL de conexión a la base de datos
- `REPORT_ENCRYPTION_KEY` — 64 caracteres hexadecimales (32 bytes)
- `ENVIRONMENT` — `development` o `production`
- `REDIS_URL` — opcional, para rate limiting distribuido

## Levantar con Docker Compose

```bash
docker compose up -d
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs

Para detener:

```bash
docker compose down
```

## Levantar manualmente

Backend:

```bash
cd src/backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Frontend:

```bash
cd src/frontend
npm run dev
```

## Tests

Backend:

```bash
cd src/backend
pytest --cov=app --cov-report=term-missing
```

Frontend unitarios:

```bash
cd src/frontend
npm test
```

Frontend E2E (navegador real):

```bash
cd src/frontend
npx playwright install chromium webkit
npm run e2e
```

Para ver la ejecución en Safari/WebKit localmente:

```bash
npm run e2e -- --project=webkit --headed
```

## CI/CD

El workflow `.github/workflows/ci.yml` ejecuta automáticamente:

- Lint y formato del backend (`ruff`, `black`)
- Tests del backend con cobertura (`pytest`)
- Tests unitarios del frontend (`vitest`)
- Build de producción del frontend (`vite build`)

## Decisiones de Arquitectura

- **AES-256-GCM:** Encriptación autenticada, detecta tampering.
- **SQLite en dev:** Rápido, sin infraestructura.
- **PostgreSQL en prod:** Escalable, con backups.
- **Rate limiting por IP:** Protección básica sin identificar usuarios.
- **Sin metadata identificable:** No se guardan IPs, user-agents, cookies ni datos de navegador.
- **Docker Compose:** Entorno de desarrollo reproducible y portable.
