# SPEC-003 — IA Triage y Clasificación (Módulo 003)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ NUEVO — Pendiente desarrollo

---

## 1. RESUMEN

El Módulo 003 implementa un sistema de Inteligencia Artificial para clasificación automática de reportes y detección de patrones de grooming. Usa NLP (Natural Language Processing) para analizar el texto del reporte, categorizar el incidente, calcular un score de riesgo (0-1), y detectar señales de grooming o engaño hacia menores.

**El modelo NO acusa.** Genera un score de "contacto inapropiado con menores reportado por la comunidad". La investigación judicial es responsabilidad exclusiva de las autoridades.

---

## 2. FUNCIONALIDADES

### 2.1 Clasificación Automática de Reportes

Al recibir un reporte, el sistema:
1. Desencripta el texto (en memoria, nunca en disco)
2. Ejecuta el modelo NLP
3. Asigna categoría (CAT-01 a CAT-06)
4. Calcula score de riesgo (0.0 - 1.0)
5. Almacena resultado encriptado (Analysis)
6. Actualiza el semáforo del identificador

### 2.2 Detección de Grooming

El modelo detecta patrones lingüísticos asociados a grooming:
- Minimización de la edad ("no es tan grave", "es solo un juego")
- Secreción ("no le digas a nadie", "es nuestro secreto")
- Aislamiento ("tus padres no entienden", "yo sí te entiendo")
- Normalización ("todos lo hacen", "es normal a tu edad")
- Progresión gradual (de amistad → confianza → solicitud material)
- Uso de lenguaje infantilizado por un adulto

### 2.3 Score de Riesgo

| Score | Nivel | Acción | Color Semáforo |
|-------|-------|--------|----------------|
| 0.0 - 0.3 | Low | Almacenar, no alerta | — |
| 0.3 - 0.5 | Medium | Almacenar, resumen semanal | — |
| 0.5 - 0.7 | High | Almacenar, alerta diaria | 🟡 |
| 0.7 - 0.85 | Critical | Almacenar, alerta inmediata | 🔴 |
| 0.85 - 1.0 | Severe | Almacenar, alerta inmediata + pasarela | ⚫ |

---

## 3. ENDPOINTS

### `POST /api/analyze/{report_id}` (async)

**Ejecutado automáticamente al recibir reporte.**

**Body:**
```json
{
  "model_version": "grooming-v1.0"
}
```

**Response 202 (Accepted):**
```json
{
  "analysis_id": "uuid",
  "status": "processing",
  "estimated_seconds": 2
}
```

**Response 200 (Completed):**
```json
{
  "analysis_id": "uuid",
  "report_id": "uuid",
  "score": 0.87,
  "level": "severe",
  "category": "CAT-03",
  "category_name": "grooming",
  "confidence": 0.92,
  "grooming_indicators": [
    "secrecion",
    "aislamiento",
    "progresion_gradual"
  ],
  "model_version": "grooming-v1.0",
  "explanation": "SHAP values o top tokens",
  "processed_at": "2026-06-13T10:30:00Z"
}
```

### `GET /api/analyze/{report_id}`

Retorna el resultado del análisis (para panel admin).

---

## 4. MODELO NLP

### 4.1 Arquitectura

```
Pipeline de Triage IA:

Texto del reporte (español, colombiano, latinoamericano)
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 1. Preprocesamiento                                │
│    • Lowercase, eliminar acentos opcional          │
│    • Tokenización (spaCy es_core_news_md)         │
│    • Eliminar stopwords (lista personalizada)      │
│    • Lematización                                  │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 2. Feature Extraction                              │
│    • TF-IDF (n-gramas 1-3)                        │
│    • Embeddings: distiluse-base-multilingual       │
│    • Features manuales: longitud, mayúsculas,      │
│      emojis, URLs, números de teléfono, etc.      │
│    • Lexicon de grooming (lista de palabras/       │
│      frases indicadoras)                            │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 3. Clasificador                                    │
│    • Ensemble: Logistic Regression + Random Forest  │
│    • Calibración de probabilidad (Platt scaling)    │
│    • AUC-ROC objetivo: ≥ 0.80                      │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 4. Explicabilidad                                  │
│    • SHAP values para tokens más importantes      │
│    • Top 5 tokens que contribuyen al score         │
│    • Indicadores de grooming detectados            │
└─────────────────────────────────────────────────────┘
           │
           ▼
Score (0-1) + Categoría + Explicación
```

### 4.2 Dataset

- **Dataset sintético:** 1,500 ejemplos etiquetados
- **Distribución:**
  - 30% CAT-01 (contacto inapropiado)
  - 20% CAT-02 (solicitud material)
  - 25% CAT-03 (grooming)
  - 15% CAT-04 (cita en persona)
  - 10% CAT-05 (extorsión)
  - 5% CAT-06 (desconocido)
- **Idioma:** Español (Colombia, México, Argentina, España)
- **Balance:** Estratificado por categoría y severidad
- **Etiquetado:** Semi-automático (keyword matching) + revisión manual

### 4.3 Fairness y Red-Teaming

- **Fairness audit:** Disparidad < 10% entre subgrupos (género, edad, tipo de contacto)
- **Red-teaming:** 0 ejemplos de alto riesgo clasificados como low
- **Bias testing:** Validar que el modelo no sesga por dialecto, género del reportante, o tipo de evidencia
- **Explainability:** Toda decisión con score > 0.7 debe incluir explicación SHAP

---

## 5. CRITERIOS DE ACEPTACIÓN (DoD)

- [ ] Pipeline de preprocesamiento funcional (español colombiano)
- [ ] Dataset sintético de 1,500 ejemplos generado y etiquetado
- [ ] Modelo entrenado con AUC-ROC ≥ 0.80 en test holdout
- [ ] Fairness audit: disparidad < 10% entre subgrupos
- [ ] Red-teaming: 0 falsos negativos de alto riesgo
- [ ] Endpoint POST /api/analyze/{report_id} funcional (async)
- [ ] Explicabilidad SHAP integrada para scores > 0.7
- [ ] Modelo versionado y reproducible (model card)
- [ ] Tests unitarios ≥ 80% cobertura
- [ ] Tiempo de inferencia < 500ms (95 percentile)
- [ ] ADR-003 aprobado (modelo NLP + dataset + fairness)
- [ ] No almacena texto desencriptado en logs ni disco

---

> *SPEC generado por ZEUS — Innovadataco*  
> *Módulo 003 — Nuevo en v2.0*
