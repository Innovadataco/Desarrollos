# PLAN-002: IA Scoring de Riesgo para Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-13  
**Autor:** ODIN  
**Estado:** Borrador — pendiente aprobación

---

## 1. STACK TECNOLÓGICO

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| Framework ML | scikit-learn 1.6+ | Ligero, interpretable, suficiente para MVP de texto. |
| Vectorización | TF-IDF | Rápido, explicable, no requiere GPU. |
| Clasificación/Scoring | Logistic Regression + Calibrated probabilities | Probabilidades calibradas, interpretación directa. |
| Explicabilidad | SHAP (o coefficients de LR como fallback) | Explica qué tokens impulsan el score. |
| Dataset | pandas + synthetic data | Preparación y validación local. |
| API IA | FastAPI endpoint `/api/analyze/{report_id}` | Reutiliza stack del backend. |
| Persistencia | SQLAlchemy (tabla `Analysis`) | Misma base de datos del backend. |
| Versionado | Modelo guardado en `src/ia/models/` + metadata JSON | Sencillo, reproducible, sin DVC/MLflow en MVP. |
| Tests | pytest + validación holdout + red-teaming | Validación técnica y ética. |

**No se usa transformers (BERT) en MVP** por costo, latencia y requisito de explicabilidad. Se reconsiderará en módulos futuros si el rendimiento no es suficiente. Ver ADR-IA-001.

---

## 2. ARQUITECTURA DE ALTO NIVEL

```
┌─────────────────────────────────────────────────────────────┐
│                     Backend FastAPI                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Módulo IA (src/backend/app/services/scoring.py)   │   │
│  │  - Carga modelo y vectorizador                      │   │
│  │  - Descifra descripción del reporte                 │   │
│  │  - Predice score y nivel                            │   │
│  │  - Genera explicación SHAP                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────────┐     │
│  │  Router /api/analyze/{report_id}                    │     │
│  │  - GET: analizar reporte                            │     │
│  │  - Persiste resultado en tabla Analysis             │     │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
              SQLite/PostgreSQL   Modelo + Vectorizador
              (tablas Report,    (pickle/joblib en
               Analysis)          src/ia/models/)
```

---

## 3. MODELO DE DATOS

### Entidad `Analysis` (nueva)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| report_id | UUID | FK → reports.id |
| score | Float | Probabilidad de riesgo [0,1] |
| level | String(20) | low / medium / high / critical |
| model_version | String(50) | Versión del modelo usado |
| explanation | JSON | SHAP values o coefficients |
| created_at | DateTime | Timestamp UTC |

### Entidad `Report` (existente)

Sin cambios estructurales. El texto se descifra en memoria únicamente durante la inferencia.

### Entidad `ModelVersion` (opcional, MVP simple)

Se representa mediante archivos versionados en `src/ia/models/` y metadatos en código.

---

## 4. API ENDPOINTS

### `GET /api/analyze/{report_id}`
Analiza un reporte existente y devuelve el score.

**Request:**
- Path param: `report_id` (UUID)

**Response 200:**
```json
{
  "report_id": "uuid",
  "score": 0.87,
  "level": "critical",
  "model_version": "risk-v1.0.0",
  "timestamp": "2026-06-13T00:00:00Z",
  "explanation": [
    {"token": "menor", "contribution": 0.12},
    {"token": "desprotegido", "contribution": 0.09}
  ]
}
```

**Response 404:** Reporte no encontrado.  
**Response 500:** Error de inferencia (fallback a no score).

### `GET /api/analyze/health`
Health check del componente IA.

**Response 200:**
```json
{
  "status": "ok",
  "model_version": "risk-v1.0.0",
  "loaded_at": "2026-06-13T00:00:00Z"
}
```

---

## 5. SEGURIDAD Y PRIVACIDAD

- El texto se descifra solo en memoria durante la inferencia.
- Los logs del modelo no almacenan texto original ni identificadores.
- El endpoint de análisis **no expone** el texto del reporte; solo score y explicación agregada.
- Rate limiting reutiliza la infraestructura existente.
- El modelo se carga una sola vez al iniciar la aplicación (singleton thread-safe).

---

## 6. ESTRATEGIA DE TESTING

| Tipo | Cobertura | Herramienta |
|------|-----------|-------------|
| Unitario del modelo | Preprocesamiento, predicción, niveles | pytest |
| Holdout validation | Train/val/test 70/15/15, métricas AUC-ROC, F1 | scikit-learn |
| Integración endpoint | `/api/analyze/{report_id}` | TestClient + pytest |
| Red-teaming | Evasión, negación, distracción, lenguaje ofensivo | pytest + dataset adversarial |
| Fairness | Disparidad entre grupos sintéticos | pytest + métricas simples |
| Cobertura | ≥ 80% del módulo IA | pytest-cov |

---

## 7. ESTRATEGIA DE DEPLOY

- El modelo se empaqueta como artefactos en `src/ia/models/`.
- Al deployar el backend, los artefactos se copian dentro de la imagen Docker.
- No se requiere servicio adicional; el scoring corre dentro del proceso FastAPI.
- Para alta carga futura, evaluar cola de jobs (Celery/RQ) o servicio independiente.

---

## 8. ESTIMACIÓN DE ESFUERZO

| Fase | Horas | Responsable |
|------|-------|-------------|
| Preparar dataset sintético | 4 | ODIN |
| Entrenar y evaluar modelo | 6 | ODIN |
| Implementar servicio de scoring | 6 | ODIN |
| Endpoint /api/analyze | 4 | ODIN |
| Explicabilidad SHAP | 4 | ODIN |
| Red-teaming + fairness | 4 | ODIN |
| Tests + cobertura | 4 | ODIN |
| Documentación (model-card, eval) | 4 | ODIN |
| **Total** | **36h** | ODIN |

---

> Generado por ODIN — Innovadataco
