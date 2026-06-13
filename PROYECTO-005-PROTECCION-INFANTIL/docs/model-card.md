# Model Card — Risk Triage v1.0.0

## Descripción
Modelo de clasificación de riesgo para reportes de contacto inapropiado con menores recibidos por la plataforma Semáforo de Confianza.

## Propósito
- Asignar un score de riesgo (0–1) a cada reporte.
- Clasificar el incidente en una de seis categorías.
- Detectar indicadores lingüísticos de grooming.
- No acusar ni identificar al reportante.

## Dataset
- **Nombre:** synthetic_train_v1.csv
- **Tamaño:** 1,800 ejemplos sintéticos.
- **Idioma:** Español latinoamericano (Colombia, México, Argentina).
- **Distribución:**
  - contacto_inapropiado: 30 %
  - solicitud_material: 20 %
  - grooming: 25 %
  - cita_persona: 15 %
  - extorsion: 10 %
  - desconocido: 5 %

## Arquitectura
- TF-IDF (n-gramas 1–3, max_features=5000).
- Ensemble: LogisticRegression + RandomForest calibrado.
- Clasificador de categoría: RandomForest.

## Métricas
- AUC-ROC: 0.9087
- F1: 0.8794

## Umbrales
- low: < 0.3
- medium: 0.3–0.5
- high: 0.5–0.7
- critical: 0.7–0.85
- severe: ≥ 0.85

## Explicabilidad
- SHAP-like: top 5 tokens con mayor peso en LogisticRegression para scores > 0.7.
- Lista de indicadores de grooming (keywords).

## Limitaciones
- Entrenado con datos sintéticos; rendimiento en texto real debe validarse.
- Puede no generalizar a todos los dialectos del español.
- No reemplaza la investigación judicial.

## Uso
El modelo se ejecuta automáticamente al recibir un reporte. También puede ejecutarse manualmente desde el panel admin.


## Auditoría y gobernanza

### Fairness
- Se evalúan variantes del mismo incidente con diferente estilo, registro y ortografía.
- Si la diferencia máxima de score (`score_spread`) supera 0.25 se levanta bandera de sesgo.
- Los análisis están disponibles en `GET /api/v1/analyze/fairness`.

### Red teaming
- Conjunto de prompts adversariales probados periódicamente.
- Objetivo: detectar evasión y falsos negativos.
- Endpoint: `GET /api/v1/analyze/redteam` (requiere supervisor).

### Actualización
- Reentrenamiento recomendado trimestral con datos reales anonimizados validados por especialistas.
- Cualquier cambio de modelo debe reflejarse en este model card y en `/api/v1/analyze/model-card`.
