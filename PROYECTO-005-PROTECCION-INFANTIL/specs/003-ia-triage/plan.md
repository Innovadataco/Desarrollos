# PLAN-003 — IA Triage y Clasificación (Módulo 003)

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Estado:** ⬜ NUEVO — Planificado agosto 2026

---

## 1. OBJETIVO

Implementar el pipeline de IA para clasificación automática de reportes, detección de grooming, y scoring de riesgo, con explicabilidad y fairness audit.

---

## 2. TAREAS

| # | Tarea | Horas | Estado | Dependencia |
|---|-------|-------|--------|-------------|
| 3.1 | Generar dataset sintético 1,500 ejemplos (español) | 8h | ⬜ | — |
| 3.2 | Implementar preprocesamiento NLP (spaCy, es_core_news_md) | 4h | ⬜ | — |
| 3.3 | Implementar feature extraction (TF-IDF + embeddings) | 6h | ⬜ | — |
| 3.4 | Implementar lexicon de grooming (indicadores) | 4h | ⬜ | — |
| 3.5 | Entrenar clasificador (Logistic Regression + Random Forest) | 6h | ⬜ | 3.1-3.4 |
| 3.6 | Calibrar probabilidad (Platt scaling) | 2h | ⬜ | 3.5 |
| 3.7 | Implementar fairness audit | 4h | ⬜ | 3.5 |
| 3.8 | Implementar red-teaming (0 falsos negativos) | 4h | ⬜ | 3.5 |
| 3.9 | Implementar explicabilidad SHAP | 4h | ⬜ | 3.5 |
| 3.10 | Implementar endpoint POST /api/analyze/{report_id} | 3h | ⬜ | TB-001.2 |
| 3.11 | Integrar análisis automático al recibir reporte | 2h | ⬜ | 3.10 |
| 3.12 | Model card + evaluation report | 3h | ⬜ | 3.5-3.9 |
| 3.13 | Tests unitarios + integración | 6h | ⬜ | — |
| **Total** | | **48h** | | |

---

## 3. HITOS

**Hito 3.1 (Ago 1-7):** Dataset + preprocesamiento  
**Hito 3.2 (Ago 8-14):** Entrenamiento + calibración  
**Hito 3.3 (Ago 15-21):** Fairness + red-teaming + SHAP  
**Hito 3.4 (Ago 22-31):** Integración + API + tests + documentación

---

## 4. DEPENDENCIAS

- Módulo 001 (Reporte) completado
- Módulo 002 (Consulta) completado
- PostgreSQL con modelo `Analysis` disponible
- Python 3.12+, spaCy, scikit-learn, transformers, shap

---

## 5. RIESGOS

| Riesgo | Mitigación |
|--------|------------|
| Dataset sesgado (dialecto, género) | Estratificación + fairness audit + red-teaming |
| Falsos positivos (score alto en reporte benigno) | Calibración Platt + threshold ajustable |
| Falsos negativos (reporte grave como low) | Red-teaming + ensemble de modelos |
| Tiempo de inferencia alto | Modelo ligero (LR + RF), no deep learning |
| Explicabilidad no útil | SHAP + top tokens + indicadores de grooming |

---

> *Plan generado por ZEUS — Innovadataco*
