# TASKS-002: IA Scoring de Riesgo para Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-13  
**Autor:** ODIN  
**Estado:** Borrador — pendiente aprobación

---

## Definición de Done (DoD)

Cada tarea se considera terminada cuando:
- El código está implementado y formateado (`black`, `ruff`).
- Los tests pasan y la cobertura del módulo IA es ≥ 80%.
- La documentación asociada está actualizada.
- Se crea un commit en rama `feature/002-ia-scoring`.

---

## Tareas

### TASK-001: Crear dataset sintético de entrenamiento
**Descripción:** Generar `src/ia/data/synthetic_train_v1.csv` con al menos 1.500 ejemplos balanceados de descripciones de reportes y etiqueta de riesgo.

**Criterios de aceptación:**
- Al menos 1.500 filas.
- Columnas: `description`, `risk_score` (0-1) o `is_high_risk` (0/1).
- Sin datos personales identificables.
- Archivo marcado como `SYNTHETIC — NOT FOR PRODUCTION USE`.

**Estimación:** 4h  
**Dependencias:** Ninguna  
**Responsable:** ODIN

---

### TASK-002: Entrenar modelo de scoring base
**Descripción:** Entrenar pipeline TF-IDF + Logistic Regression calibrada, guardar artefactos en `src/ia/models/risk-v1.0.0/`.

**Criterios de aceptación:**
- Train/val/test 70/15/15.
- AUC-ROC ≥ 0.80 en test.
- F1 ≥ 0.75 en clase de alto riesgo (si binario).
- Archivos: `model.joblib`, `vectorizer.joblib`, `metadata.json`.

**Estimación:** 6h  
**Dependencias:** TASK-001  
**Responsable:** ODIN

---

### TASK-003: Crear servicio de scoring en backend
**Descripción:** Implementar `src/backend/app/services/scoring.py` que cargue el modelo, descifre la descripción, prediga score y nivel, y genere explicación.

**Criterios de aceptación:**
- Carga lazy y thread-safe del modelo.
- Función `analyze_report(report: Report) -> AnalysisResult`.
- Mapeo de score a niveles según RN-006.
- Explicación con coefficients de LR u SHAP.
- No expone texto original en logs.

**Estimación:** 6h  
**Dependencias:** TASK-002  
**Responsable:** ODIN

---

### TASK-004: Crear modelo de datos Analysis
**Descripción:** Añadir entidad `Analysis` en `src/backend/app/models.py` con migración implícita (SQLite/PostgreSQL con SQLAlchemy).

**Criterios de aceptación:**
- Campos: id, report_id (FK), score, level, model_version, explanation (JSON), created_at.
- Relación con Report.
- Tests de modelo.

**Estimación:** 3h  
**Dependencias:** TASK-003  
**Responsable:** ODIN

---

### TASK-005: Implementar endpoint /api/analyze/{report_id}
**Descripción:** Crear router `src/backend/app/routers/analyze.py` y registrarlo en `app.main`.

**Criterios de aceptación:**
- GET /api/analyze/{report_id} devuelve score, nivel, versión, timestamp y explicación.
- Persiste resultado en tabla Analysis.
- Maneja 404 si reporte no existe.
- Rate limit reutilizado.
- Tests de integración con TestClient.

**Estimación:** 4h  
**Dependencias:** TASK-003, TASK-004  
**Responsable:** ODIN

---

### TASK-006: Implementar health check de IA
**Descripción:** Endpoint `/api/analyze/health` que confirme que el modelo está cargado.

**Criterios de aceptación:**
- Devuelve status ok, model_version y loaded_at.
- Test de integración.

**Estimación:** 1h  
**Dependencias:** TASK-005  
**Responsable:** ODIN

---

### TASK-007: Red-teaming del modelo
**Descripción:** Crear dataset adversarial y tests para evaluar robustez ante evasión, negación y distracción.

**Criterios de aceptación:**
- Al menos 20 ejemplos adversariales.
- Documento `src/ia/docs/red-teaming.md` con hallazgos.
- Ningún ejemplo de alto riesgo sea clasificado como `low`.

**Estimación:** 4h  
**Dependencias:** TASK-002  
**Responsable:** ODIN

---

### TASK-008: Auditoría de fairness
**Descripción:** Evaluar que el modelo no discrimine por género del menor, zona o tipo de lenguaje usando subgrupos sintéticos.

**Criterios de aceptación:**
- Documento `src/ia/docs/fairness.md`.
- Diferencia de recall entre subgrupos < 10%.
- Tests automatizados de fairness.

**Estimación:** 4h  
**Dependencias:** TASK-002  
**Responsable:** ODIN

---

### TASK-009: Model card y evaluation report
**Descripción:** Documentar modelo en `src/ia/docs/model-card.md` y evaluación en `src/ia/docs/evaluation.md`.

**Criterios de aceptación:**
- model-card con propósito, limitaciones, datos, métricas, riesgos éticos.
- evaluation con gráficas/métricas holdout.

**Estimación:** 3h  
**Dependencias:** TASK-002, TASK-007, TASK-008  
**Responsable:** ODIN

---

### TASK-010: Integrar dependencias y actualizar CI
**Descripción:** Añadir `scikit-learn`, `pandas`, `joblib`, `shap` a requirements.txt y pasos de CI.

**Criterios de aceptación:**
- requirements.txt actualizado.
- CI ejecuta tests del módulo IA.
- Build de frontend sigue funcionando.

**Estimación:** 2h  
**Dependencias:** TASK-005  
**Responsable:** ODIN

---

## Cronograma sugerido

| Día | Tareas |
|-----|--------|
| 1 | TASK-001, TASK-002 |
| 2 | TASK-003, TASK-004 |
| 3 | TASK-005, TASK-006, TASK-010 |
| 4 | TASK-007, TASK-008 |
| 5 | TASK-009, refactor, PR |

---

> Generado por ODIN — Innovadataco
