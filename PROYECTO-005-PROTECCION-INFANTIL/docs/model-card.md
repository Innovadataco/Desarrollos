# Model Card — Risk Triage v1.0.0

## Descripción
Modelo de clasificación de riesgo para reportes de contacto inapropiado con menores recibidos por la plataforma Semáforo de Confianza.

## Propósito
- Asignar un score de riesgo (0–1) a cada reporte.
- Clasificar el incidente en una de seis categorías.
- Detectar indicadores lingüísticos de grooming.
- No acusar ni identificar al reportante.

## Versión
`risk-v1.0.0`

## Dataset
- **Nombre:** `ia/data/dataset.csv`
- **Tamaño:** 1.500 ejemplos sintéticos.
- **Idioma:** Español latinoamericano (Colombia, México, Argentina).
- **Distribución:**
  - contacto_inapropiado: 30 %
  - solicitud_material: 20 %
  - grooming: 25 %
  - cita_persona: 15 %
  - extorsion: 10 %
  - desconocido: 5 %
- **Split:** 70 % entrenamiento, 15 % validación, 15 % test.

## Arquitectura
- Preprocesamiento: lowercase, eliminación de acentos y puntuación, stopwords personalizadas.
- TF-IDF: n-gramas 1–3, `max_features=4000`, `sublinear_tf=True`.
- Ensemble de riesgo:
  - LogisticRegression calibrada (Platt, cv=5).
  - RandomForest calibrado (Platt, cv=3).
  - Score final: promedio de ambas probabilidades.
- Clasificador de categoría: LogisticRegression multiclase.

## Métricas (test holdout)
| Métrica | Valor |
|---------|-------|
| AUC-ROC | 0.9997 |
| Precision | 0.9930 |
| Recall | 0.9860 |
| F1 | 0.9895 |
| Accuracy (riesgo) | 0.9867 |
| Accuracy (categoría) | 1.0000 |
| F1-macro (categoría) | 1.0000 |

## Umbrales
| Nivel | Score | Acción |
|-------|-------|--------|
| low | < 0.30 | Almacenar, sin alerta |
| medium | 0.30–0.50 | Almacenar, resumen semanal |
| high | 0.50–0.70 | Almacenar, alerta diaria |
| critical | 0.70–0.85 | Almacenar, alerta inmediata |
| severe | ≥ 0.85 | Almacenar, alerta inmediata + pasarela |

## Explicabilidad
- Top 5 tokens con mayor peso positivo en la regresión logística para scores > 0.7.
- Lista de indicadores de grooming detectados por keyword matching.

## Limitaciones
- Entrenado con datos sintéticos; rendimiento en texto real debe validarse.
- Puede no generalizar a todos los dialectos del español.
- Textos sin tokens reconocidos reciben score 0.0 como medida conservadora.
- No reemplaza la investigación judicial.

## Uso
El modelo se ejecuta automáticamente al recibir un reporte (`POST /api/v1/reportes`). También puede ejecutarse manualmente desde el panel admin (`POST /api/v1/analyze/{report_id}`). La información del modelo está disponible en `GET /api/v1/analyze/model-card`.

## Auditoría y gobernanza

### Fairness
- Se evalúan variantes del mismo incidente con diferente estilo, registro y ortografía.
- Máxima dispersión observada: 0.0185 (1.85 %).
- Endpoint: `GET /api/v1/analyze/fairness`.

### Red teaming
- Conjunto de prompts adversariales probados periódicamente.
- Resultado: 0 falsos negativos en prompts de alto riesgo.
- Endpoint: `GET /api/v1/analyze/redteam` (requiere supervisor).

### Actualización
- Reentrenamiento recomendado trimestral con datos reales anonimizados validados por especialistas.
- Cualquier cambio de modelo debe reflejarse en este model card y en `/api/v1/analyze/model-card`.
