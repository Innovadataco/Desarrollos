# TASKS-003 — IA Triage (Módulo 003)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Pendientes

---

## 1. DATASET Y ENTRENAMIENTO

- [ ] `TML-003.1` Generar dataset sintético 1,500 ejemplos (español colombiano/mexicano/argentino)
- [ ] `TML-003.2` Estratificar por categoría (CAT-01 a CAT-06) y severidad
- [ ] `TML-003.3` Etiquetar semi-automáticamente (keyword matching) + revisión manual
- [ ] `TML-003.4` Split train/val/test (70/15/15)
- [ ] `TML-003.5` Guardar dataset versionado (DVC o git LFS)

## 2. PREPROCESAMIENTO Y FEATURES

- [ ] `TML-003.6` Instalar spaCy + modelo es_core_news_md
- [ ] `TML-003.7` Implementar preprocesamiento (tokenización, lematización, stopwords)
- [ ] `TML-003.8` Implementar TF-IDF vectorizer (n-grams 1-3)
- [ ] `TML-003.9` Implementar embeddings (distiluse-base-multilingual, opcional)
- [ ] `TML-003.10` Implementar features manuales (longitud, emojis, URLs, teléfonos)
- [ ] `TML-003.11` Implementar lexicon de grooming (lista de palabras/frases indicadoras)

## 3. MODELO Y EVALUACIÓN

- [ ] `TML-003.12` Entrenar Logistic Regression (baseline)
- [ ] `TML-003.13` Entrenar Random Forest (ensemble)
- [ ] `TML-003.14` Implementar ensemble (voting o stacking)
- [ ] `TML-003.15` Calibrar probabilidad con Platt scaling
- [ ] `TML-003.16` Evaluar AUC-ROC en test (objetivo ≥ 0.80)
- [ ] `TML-003.17` Fairness audit: disparidad < 10% entre subgrupos
- [ ] `TML-003.18` Red-teaming: 0 falsos negativos de alto riesgo
- [ ] `TML-003.19` Model card (objetivo, dataset, métricas, limitaciones)

## 4. EXPLICABILIDAD

- [ ] `TML-003.20` Integrar SHAP para explicación de tokens
- [ ] `TML-003.21` Implementar top 5 tokens que contribuyen al score
- [ ] `TML-003.22` Implementar detección de indicadores de grooming
- [ ] `TML-003.23` Explicación solo para scores > 0.7 (performance)

## 5. BACKEND INTEGRACIÓN

- [ ] `TB-003.1` Implementar modelo `Analysis` (SQLAlchemy)
- [ ] `TB-003.2` Implementar endpoint POST /api/analyze/{report_id} (async)
- [ ] `TB-003.3` Implementar endpoint GET /api/analyze/{report_id}
- [ ] `TB-003.4` Integrar análisis automático en POST /api/reportes (webhook interno)
- [ ] `TB-003.5` Modelo versionado en código (model_version string)
- [ ] `TB-003.6` No almacenar texto desencriptado en logs ni disco
- [ ] `TB-003.7` Tests unitarios (pytest, cobertura ≥ 80%)
- [ ] `TB-003.8` Tests de integración (TestClient)

## 6. DOCUMENTACIÓN

- [ ] `TD-003.1` ADR-003: Decisión de modelo NLP + dataset + fairness
- [ ] `TD-003.2` Model card (docs/model-card.md)
- [ ] `TD-003.3` Evaluation report (docs/evaluation.md)
- [ ] `TD-003.4` Red-teaming report (docs/red-teaming.md)
- [ ] `TD-003.5` Fairness report (docs/fairness.md)

---

> *Tasks generados por ZEUS — Innovadataco*
