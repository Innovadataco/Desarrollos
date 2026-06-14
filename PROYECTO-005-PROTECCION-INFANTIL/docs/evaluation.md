# Evaluation Report — Módulo 003 IA Triage

**Modelo:** `risk-v1.0.0`  
**Dataset:** `ia/data/dataset.csv`  
**Fecha de entrenamiento:** 2026-06-13  
**Script:** `scripts/train_model.py`

---

## 1. Dataset

- **Tamaño total:** 1.500 ejemplos sintéticos en español latinoamericano.
- **Distribución por categoría:**
  - `contacto_inapropiado`: 30 %
  - `solicitud_material`: 20 %
  - `grooming`: 25 %
  - `cita_persona`: 15 %
  - `extorsion`: 10 %
  - `desconocido`: 5 %
- **Split:** 70 % train (1.050), 15 % validation (225), 15 % test (225).
- **Estratificación:** por categoría en el split train/val+test; por riesgo en el split val/test.
- **Augmentación:** variantes dialectales (colombiano, mexicano, argentino), registro formal/coloquial, errores ortográficos leves y sinónimos.

## 2. Preprocesamiento y features

- Lowercase, eliminación de acentos y puntuación.
- Stopwords personalizadas en español (artículos, preposiciones, conjunciones).
- TF-IDF con n-gramas 1–3, `max_features=4000`, `sublinear_tf=True`.

## 3. Modelos entrenados

| Modelo | Tipo | Uso |
|--------|------|-----|
| `model_lr.joblib` | LogisticRegression + CalibratedClassifierCV (Platt) | Probabilidad de riesgo |
| `model_rf.joblib` | RandomForest + CalibratedClassifierCV (Platt) | Probabilidad de riesgo |
| `model_category.joblib` | LogisticRegression multiclase | Clasificación de categoría |
| `vectorizer.joblib` | TfidfVectorizer | Vectorización de texto |

## 4. Métricas en test holdout

### Riesgo (clasificación binaria)
| Métrica | Valor |
|---------|-------|
| AUC-ROC | 0.9997 |
| Precision | 0.9930 |
| Recall | 0.9860 |
| F1 | 0.9895 |
| Accuracy | 0.9867 |

### Categoría (clasificación multiclase)
| Métrica | Valor |
|---------|-------|
| Accuracy | 1.0000 |
| F1-macro | 1.0000 |

## 5. Interpretación

- El ensemble LR+RF alcanza un AUC-ROC muy superior al umbral mínimo de 0.80 definido en el SPEC-003.
- El recall de 0.9860 indica que casi todos los casos de alto riesgo del test son detectados.
- El clasificador de categoría separa correctamente las seis categorías en el conjunto de test sintético.

## 6. Limitaciones observadas

- Las métricas reflejan rendimiento sobre datos sintéticos; se espera degradación controlada en texto real.
- Textos sin tokens del vocabulario aprendido reciben score 0.0 como comportamiento conservador.
- El modelo depende de la presencia de palabras clave; frases extremadamente implícitas pueden no ser detectadas.

## 7. Recomendaciones

- Validar con datos reales anonimizados tan pronto como estén disponibles.
- Monitorear métricas de producción y reentrenar trimestralmente.
- Considerar embeddings multilingües como feature adicional en futuras versiones.
