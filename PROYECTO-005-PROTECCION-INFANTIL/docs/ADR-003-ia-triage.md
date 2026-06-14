# ADR-003 — Modelo NLP para Triage de Reportes

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ✅ Aprobado

---

## Contexto

El sistema recibe reportes en texto libre en español (colombiano, mexicano, argentino). Necesita clasificar automáticamente el tipo de incidente, calcular un score de riesgo, y detectar patrones de grooming, sin sesgar por dialecto, género, o tipo de evidencia.

## Decisión

**Usar un ensemble de Logistic Regression + Random Forest con TF-IDF (n-gramas 1-3), entrenado en un dataset sintético de 1.500 ejemplos en español, con calibración Platt, auditoría de fairness y explicabilidad por pesos del modelo.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| Logistic Regression + TF-IDF | Rápido, interpretable, ligero | Menor capacidad para patrones complejos | ✅ Elegido (baseline) |
| Random Forest + TF-IDF | Mejor captura de interacciones | Menos interpretable | ✅ Elegido (ensemble) |
| BERT/RoBERTa (multilingual) | State-of-the-art para NLP | Muy lento para inferencia en tiempo real (~500ms), dependencia de GPU, riesgo de overfitting en dataset pequeño | ❌ Rechazado (futuro) |
| LLM (GPT-4 API) | Muy preciso, no requiere entrenamiento | Costo por inferencia, latencia alta, dependencia de proveedor externo, privacidad de datos sensibles | ❌ Rechazado |
| Keyword matching simple | Ultra-rápido, fácil | Muy inexacto, falsos positivos/negativos masivos | ❌ Rechazado |

## Razonamiento

1. **Velocidad:** El modelo debe inferir en <500ms en CPU. LR+RF en CPU es ~50ms. BERT en CPU es ~2s. LLM API es ~1s + red.
2. **Privacidad:** El texto del reporte se procesa en memoria del servidor. No sale a APIs externas. Un LLM API requeriría enviar texto sensible a terceros.
3. **Interpretabilidad:** Los pesos de LR permiten generar un top-5 de tokens sin depender de SHAP en runtime.
4. **Dataset pequeño:** 1.500 ejemplos es insuficiente para BERT (necesita 10.000+). Es suficiente para LR+RF con regularización.
5. **Mantenibilidad:** LR+RF se puede entrenar en cualquier laptop en minutos. BERT requiere GPU.
6. **Fairness:** LR+RF es más fácil de auditar por fairness. BERT es caja negra.

## Consecuencias

### Positivas
- Rápido: ~50ms inferencia en CPU.
- Interpretable: top tokens e indicadores de grooming.
- Privado: todo en servidor local.
- Mantenible: entrenamiento reproducible con `scripts/train_model.py`.
- Económico: $0 de API calls.

### Negativas
- Menor precisión que BERT/LLM (aceptable: AUC-ROC ≥0.80).
- Dataset sintético puede no capturar todos los dialectos (mitigado con fairness audit).
- Requiere reentrenamiento periódico con datos reales anonimizados.

## Implementación

```text
scripts/train_model.py
├── Genera ia/data/dataset.csv (1.500 ejemplos)
├── Preprocesa: lowercase, eliminación de acentos, puntuación, stopwords personalizadas
├── Vectoriza: TfidfVectorizer(ngram_range=(1,3), max_features=4000)
├── Entrena:
│   ├── LR calibrado (Platt) para score de riesgo
│   ├── RF calibrado (Platt) para score de riesgo
│   └── LR multiclase para categoría
├── Evalúa: AUC-ROC, precision, recall, f1, accuracy
├── Audita: fairness (dispersión <10%) y red-team (0 falsos negativos)
└── Guarda artefactos en ia/models/risk-v1.0.0/
```

```python
# Runtime (src/backend/app/services/scoring.py)
processed = _preprocess(text)
vec = vectorizer.transform([processed])
score = (lr.predict_proba(vec)[0,1] + rf.predict_proba(vec)[0,1]) / 2
category = category_model.predict(vec)[0]
```

## Dataset

- **Nombre:** `ia/data/dataset.csv`
- **Tamaño:** 1.500 ejemplos sintéticos.
- **Idioma:** Español latinoamericano (Colombia, México, Argentina).
- **Distribución por categoría:**
  - contacto_inapropiado: 30 %
  - solicitud_material: 20 %
  - grooming: 25 %
  - cita_persona: 15 %
  - extorsion: 10 %
  - desconocido: 5 %
- **Estratificación:** 70 % train, 15 % validation, 15 % test.
- **Augmentación:** variantes dialectales, formales, coloquiales, con errores ortográficos y sinónimos, aplicadas solo en entrenamiento.

## Fairness

- **Grupos protegidos:** Variantes de estilo, registro formal/coloquial, marcadores dialectales.
- **Métrica:** Dispersión absoluta y relativa de score < 10 % entre variantes de la misma situación.
- **Auditoría:** Red-teaming con 0 falsos negativos de alto riesgo.
- **Mitigación:** Si la dispersión supera el umbral, se reentrena con más ejemplos del subgrupo afectado.

## Notas

- Modelo versionado: `risk-v1.0.0`.
- Model card obligatorio: `docs/model-card.md`.
- Evaluation report: `docs/evaluation.md`.
- Red-teaming report: `docs/red-teaming.md`.
- Fairness report: `docs/fairness.md`.
- Re-entrenamiento recomendado trimestral o cuando se acumulen 500 reportes reales (con consentimiento para uso en ML).
- Embeddings distiluse-base-multilingual quedan como mejora futura; no son requeridos para el MVP.

---

> *ADR generado por ZEUS — Innovadataco*  
> *Módulo 003 — IA Triage*
