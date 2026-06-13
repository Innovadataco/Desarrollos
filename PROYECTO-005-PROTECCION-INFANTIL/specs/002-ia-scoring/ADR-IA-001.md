# ADR-IA-001: Arquitectura del Modelo de Scoring de Riesgo

## Proyecto: 005 — Protección Infantil Comunitaria
**Fecha:** 2026-06-13  
**Autor:** ODIN  
**Estado:** Propuesto

---

## Contexto

El Proyecto 005 requiere priorizar reportes anónimos de protección infantil según su nivel de riesgo. El componente IA debe:
- Ser rápido (< 500ms por predicción).
- Ser explicable (autoridades deben entender el score).
- Ser reproducible y versionable.
- No requerir infraestructura de GPU en MVP.
- Operar sin exponer datos sensibles.

## Opciones consideradas

| Opción | Pros | Contras |
|--------|------|---------|
| **A. TF-IDF + Logistic Regression** | Ligero, rápido, interpretable, probabilidades calibrables, fácil de mantener. | Menor capacidad de capturar contexto complejo. |
| **B. Transformers (DistilBERT)** | Mejor comprensión semántica. | Requiere GPU/CPU intensiva, latencia alta, más difícil de explicar, dependencias pesadas. |
| **C. XGBoost + TF-IDF** | Buen rendimiento, maneja no linealidad. | Menos interpretable, riesgo de overfitting con pocos datos. |

## Decisión

**Opción A: TF-IDF + Logistic Regression calibrada** para el MVP del módulo 002.

## Justificación

1. **Suficiencia:** Las descripciones de reportes suelen contener palabras clave de riesgo directamente observables ("menor", "desprotegido", "agresión", etc.). TF-IDF + LR captura estas señales de forma robusta.
2. **Interpretabilidad:** Los coefficients de LR permiten explicar qué tokens aumentan o disminuyen el score sin depender de SHAP exclusivamente.
3. **Latencia:** La predicción es casi inmediata en CPU, cumpliendo RNF-006.
4. **Costo:** No requiere GPU ni modelos grandes, alineado con el presupuesto y alcance del MVP.
5. **Mantenibilidad:** El stack es estándar y bien documentado en ODIN-IA.

## Consecuencias

- Positivas: MVP rápido, transparente, testeable, portable.
- Negativas: Límite en comprensión de contexto sutil. Se monitoreará AUC-ROC en producción; si cae bajo 0.80, se evaluará Opción B o C.

## Consideraciones éticas

- El modelo es asistencial; **no toma decisiones** sobre menores.
- Score > 0.85 (`critical`) obliga revisión humana prioritaria.
- Se auditará fairness antes de cada release.
- No se entrenará con datos de producción sin anonimización y aprobación explícita.

## Notas

- El dataset de entrenamiento inicial es **sintético** y se etiquetará claramente como tal.
- La versión del modelo se guardará en `src/ia/models/risk-v1.0.0/`.

---

> Generado por ODIN — Innovadataco
