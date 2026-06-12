# ODIN-IA
## Metodología de Desarrollo de Componentes IA — Innovadataco
**Basada en:** CRISP-DM 1.0 (IBM/SPSS) + ADLC (IBM/EPAM)  
**Para:** Modelos de scoring, clasificación, detección, análisis de texto/imagen  
**Agente:** ODIN (Kimi Code CLI)  
**Gobernanza:** ZEUS (PM2 + ética) + Jelkin (CEO)

---

## 1. FILOSOFÍA

**"Un modelo de IA que no sabes cómo falla, es un riesgo, no una feature."**

- La IA es un componente, no el producto completo (salvo que se defina así)
- Todo modelo debe ser evaluado, no solo entrenado
- Red-teaming obligatorio: intentar romper el modelo antes de deploy
- Monitoreo post-deploy: la IA se degrada con el tiempo (data drift)
- Transparencia: se debe poder explicar por qué el modelo dio X resultado

---

## 2. CICLO DE VIDA (7 FASES)

### FASE 1: HIPÓTESIS Y ALCANCE — 1-2 días
**Qué:** ¿Qué problema resuelve la IA? ¿Tienes datos? ¿Cuántos?  
**Output:** `docs/ia/hipotesis.md` + OPM2-02

### FASE 2: ARQUITECTURA IA — 2-3 días
**Qué:** Tipo de modelo, stack ML, métricas de éxito, límites  
**Output:** `docs/ia/adr-ia-001.md` (Architecture Decision Record IA)

### FASE 3: DATOS — 3-5 días
**Qué:** Calidad, balance, sesgos, anonimización, consentimiento  
**Output:** `docs/ia/data-card.md` + datasets versionados (DVC)

### FASE 4: ENTRENAMIENTO — 3-7 días
**Qué:** Entrenar modelos candidatos, evaluar con métricas, documentar  
**Output:** `docs/ia/model-card.md` + `docs/ia/evaluation.md`

### FASE 5: RED-TEAMING — 2-3 días
**Qué:** Intentar romper el modelo: adversarial inputs, prompt injection, evasión  
**Output:** `docs/ia/red-teaming.md`

### FASE 6: INTEGRACIÓN — 2-3 días
**Qué:** API endpoint, fallback, throttling, logging, A/B testing, canary release  
**Output:** API funcional + `docs/ia/deploy.md`

### FASE 7: MONITOREO — Continuo
**Qué:** Accuracy en producción, data drift, latencia, costo, auditoría ética  
**Output:** Dashboards + `docs/ia/monitoring.md` + OPM2-19 trimestral

---

## 3. STACK DE IA

| Componente | Tecnología | Uso |
|------------|-----------|-----|
| Clasificación texto | scikit-learn + TF-IDF / transformers (DistilBERT) | Análisis de descripciones |
| Clasificación imagen | transformers (ViT, CLIP) | Análisis de evidencias |
| Scoring | XGBoost / Regresión Logística | Calcular probabilidad de riesgo |
| Explicabilidad | SHAP + LIME | Explicar por qué un score es alto |
| Monitoreo | Evidently AI | Detectar data drift |
| Versionado | MLflow / DVC | Versionar modelos y datasets |

---

## 4. ESTÁNDARES ESPECÍFICOS DE IA

### Dataset
- Mínimo 1000 ejemplos por clase (clasificación binaria)
- Train/Val/Test: 70/15/15
- Versionar con DVC
- Nunca usar datos de producción sin anonimizar

### Modelo
- Justificar algoritmo en ADR
- Hyperparámetros versionados
- Random seed fijado para reproducibilidad
- Guardar en ONNX, Pickle, o SavedModel

### Evaluación
- Métricas: Accuracy, Precision, Recall, F1, AUC-ROC
- Si desbalanceado: usar F1 y AUC-ROC (no accuracy)
- Si afecta personas: Fairness Metrics (demographic parity, equalized odds)
- Documentar falsos positivos/negativos con ejemplos

### Explicabilidad
- SHAP values: ¿qué features influyeron?
- LIME: explicación local por predicción
- Feature importance: ranking de variables

### Ética (especial para Protección Infantil)
- **No determinismo:** El modelo da probabilidades, no verdades absolutas
- **Validación humana:** Score > 80 requiere revisión humana
- **No discriminación:** Auditar que no sesga por género, etnia, zona
- **Derecho al olvido:** Reportes falsos deben poder eliminarse
- **Consentimiento:** Datos anónimos pueden usarse para reentrenar

---

## 5. INTEGRACIÓN CON ODIN-TRAD

```
┌─────────────────────────────────────┐
│         PRODUCTO TRADICIONAL        │
│  (React + FastAPI + PostgreSQL)     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   COMPONENTE IA (ODIN-IA)   │   │
│  │   - Endpoint /api/analyze │   │
│  │   - Modelo de scoring       │   │
│  │   - Explicabilidad SHAP     │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   LÓGICA DE NEGOCIO         │   │
│  │   (ODIN-TRAD)               │   │
│  │   - CRUD, Auth, UI, etc.    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

> "La IA es un componente poderoso. Documentado, evaluado y monitoreado."
> ODIN-IA — Inteligencia Artificial Responsable
