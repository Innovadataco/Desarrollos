# ADR-003 — Modelo NLP para Triage de Reportes

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ Pendiente aprobación

---

## Contexto

El sistema recibe reportes en texto libre en español (colombiano, mexicano, argentino). Necesita clasificar automáticamente el tipo de incidente, calcular un score de riesgo, y detectar patrones de grooming, sin sesgar por dialecto, género, o tipo de evidencia.

## Decisión

**Usar un ensemble de Logistic Regression + Random Forest con TF-IDF features y embeddings opcionales, entrenado en dataset sintético de 1,500 ejemplos en español, con explicabilidad SHAP.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| Logistic Regression + TF-IDF | Rápido, interpretable, ligero | Menor capacidad para patrones complejos | ✅ Elegido (baseline) |
| Random Forest + TF-IDF | Mejor captura de interacciones | Más lento, menos interpretable | ✅ Elegido (ensemble) |
| BERT/RoBERTa (multilingual) | State-of-the-art para NLP | Muy lento para inferencia en tiempo real (~500ms), dependencia de GPU, riesgo de overfitting en dataset pequeño | ❌ Rechazado (futuro) |
| LLM (GPT-4 API) | Muy preciso, no requiere entrenamiento | Costo por inferencia, latencia alta, dependencia de proveedor externo, privacidad de datos sensibles | ❌ Rechazado |
| Keyword matching simple | Ultra-rápido, fácil | Muy inexacto, falsos positivos/negativos masivos | ❌ Rechazado |

## Razonamiento

1. **Velocidad:** El modelo debe inferir en <500ms en CPU. LR+RF en CPU es ~50ms. BERT en CPU es ~2s. LLM API es ~1s + red.
2. **Privacidad:** El texto del reporte se procesa en memoria del servidor. No sale a APIs externas. Un LLM API requeriría enviar texto sensible a terceros.
3. **Interpretabilidad:** SHAP sobre LR+RF es directo. SHAP sobre BERT es complejo y costoso.
4. **Dataset pequeño:** 1,500 ejemplos es insuficiente para BERT (necesita 10,000+). Es suficiente para LR+RF con regularización.
5. **Mantenibilidad:** LR+RF se puede entrenar en cualquier laptop en minutos. BERT requiere GPU.
6. **Fairness:** LR+RF es más fácil de auditar por fairness. BERT es caja negra.

## Consecuencias

### Positivas
- Rápido: 50ms inferencia en CPU
- Interpretable: SHAP explica cada decisión
- Privado: todo en servidor local
- Mantenible: entrenamiento en minutos
- Económico: $0 de API calls

### Negativas
- Menor precisión que BERT/LLM (aceptable: AUC-ROC ≥0.80 vs 0.92 de BERT)
- Dataset sintético puede no capturar todos los dialectos (mitigado con fairness audit)
- No entiende contexto semántico profundo (mitigado con embeddings distiluse)

## Implementación

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
import shap

# Pipeline
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    max_features=10000,
    stop_words=spanish_stopwords_custom
)

X_train = vectorizer.fit_transform(texts_train)
X_test = vectorizer.transform(texts_test)

# Modelos
lr = CalibratedClassifierCV(LogisticRegression(max_iter=1000, C=0.5), cv=5)
rf = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=5)

# Ensemble
ensemble = VotingClassifier(
    estimators=[('lr', lr), ('rf', rf)],
    voting='soft'
)

ensemble.fit(X_train, y_train)

# Fairness audit
for group in ['dialecto', 'genero_reportado', 'tipo_evidencia']:
    scores = cross_val_score(ensemble, X_test_group, y_test_group, scoring='roc_auc')
    assert disparity < 0.10  # Disparidad < 10% entre subgrupos

# Explicabilidad
explainer = shap.LinearExplainer(lr, X_train)
shap_values = explainer.shap_values(X_instance)
```

## Dataset

- 1,500 ejemplos sintéticos en español (Colombia, México, Argentina, España)
- Estratificado por categoría (CAT-01 a CAT-06) y severidad
- Etiquetado semi-automático (keyword matching) + revisión manual
- Versionado con DVC o git LFS
- Data augmentation: back-translation, synonym replacement, paraphrasing

## Fairness

- **Grupos protegidos:** Dialecto, género del reportante (si mencionado), tipo de evidencia
- **Métrica:** Disparidad de AUC-ROC < 10% entre subgrupos
- **Auditoría:** Red-teaming con 0 falsos negativos de alto riesgo
- **Mitigación:** Si disparidad > 10%, re-entrenar con pesos por grupo o data augmentation

## Notas

- Modelo versionado en código: `model_version = "grooming-v1.0"`
- Model card obligatorio: objetivo, dataset, métricas, limitaciones, riesgos
- Re-entrenamiento trimestral o cuando se acumulan 500 reportes reales (con consentimiento para uso en ML)
- Embeddings distiluse-base-multilingual opcional (feature adicional, no requerido para MVP)

---

> *ADR generado por ZEUS — Innovadataco*  
> *Módulo 003 — IA Triage*
