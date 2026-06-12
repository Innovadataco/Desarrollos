# PROYECTO-005: Protección Infantil Comunitaria

**Gestión del proyecto:** IDC_PROYECTOS/PROYECTO-005-2026-PROTECCION-INFANTIL

**Cliente:** Innovadataco (producto propio)
**Director:** Jelkin Zair Carrillo Franco
**Metodología PM2:** Ver artefactos en IDC_PROYECTOS
**Metodología desarrollo:** SDD (Spec-Driven Development)
**Agente desarrollo:** ODIN (Kimi Code CLI)

## Stack Tecnológico
- Frontend: React 19 + Vite + Tailwind CSS + PWA
- Backend: FastAPI (Python)
- Base de datos: PostgreSQL 16 + SQLAlchemy 2
- IA: scikit-learn / transformers (scoring de riesgo)
- Tests: pytest + Vitest + Playwright
- DevOps: Docker + Docker Compose + GitHub Actions

## Módulo 1: Registro Anónimo

Este módulo permite registrar reportes de protección infantil de forma completamente anónima. No se almacenan IPs, cookies, user-agents ni ninguna metadata del reportante. Los datos sensibles se encriptan en reposo con AES-256-GCM usando una DEK aleatoria por campo y una KEK derivada de `REPORT_ENCRYPTION_KEY`.

### Estructura del backend

```
src/backend/
├── app/
│   ├── config.py              # Variables de entorno con pydantic-settings
│   ├── database.py            # Engine, SessionLocal y Base SQLAlchemy
│   ├── main.py                # Aplicación FastAPI, CORS, OpenAPI
│   ├── models.py              # Modelo Report (sin metadata del reportante)
│   ├── routers/
│   │   └── reportes.py        # POST /api/reportes, GET /api/health
│   ├── schemas.py             # Esquemas Pydantic
│   └── services/
│       ├── encryption.py      # AES-256-GCM, DEK/KEK, hash de reporte
│       └── rate_limit.py      # Rate limiting en memoria (5 req/hora/IP)
└── tests/
    ├── conftest.py
    ├── test_encryption.py
    └── test_reportes.py
```

### Variables de entorno

Copia `.env.example` a `.env` y ajusta los valores:

```bash
DATABASE_URL=postgresql://innovadataco:innovadataco_dev@localhost:5432/proteccion_infantil
REPORT_ENCRYPTION_KEY=<64 caracteres hex = 32 bytes>
```

Genera una clave segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Instalación local

Backend:

```bash
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Frontend:

```bash
cd src/frontend
npm install
```

### Ejecutar tests

Backend (TDD):

```bash
cd src/backend
source .venv/bin/activate
pytest -v
```

Frontend:

```bash
cd src/frontend
npm test
```

### Ejecutar localmente

Backend:

```bash
cd src/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Documentación OpenAPI: http://localhost:8000/docs

Frontend:

```bash
cd src/frontend
npm run dev
```

La aplicación estará en http://localhost:5173.

### Docker Compose

```bash
cp .env.example .env
# Ajusta REPORT_ENCRYPTION_KEY en .env
docker compose up --build -d
```

Servicios:
- PostgreSQL en `localhost:5432`
- Backend en `http://localhost:8000`
- Frontend en `http://localhost:5173`

### Criterios de aceptación validados

- [x] Formulario accesible desde móvil sin registro.
- [x] Reporte creado en BD con campos sensibles encriptados.
- [x] No queda registro de IP, cookies ni metadata del reportante.
- [x] `report_hash` único y no rastreable (SHA-256 con nonce aleatorio + reintentos ante colisiones).
- [x] Tests unitarios pasan al 100%.
- [x] Documentación OpenAPI generada en `/docs`.
