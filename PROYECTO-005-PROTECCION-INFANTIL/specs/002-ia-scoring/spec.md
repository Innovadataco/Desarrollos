# SPEC-002: IA Scoring de Riesgo para Reportes

## Proyecto: 005 — Protección Infantil Comunitaria
**Versión:** 1.0.0  
**Fecha:** 2026-06-13  
**Autor:** ODIN (CEO IA Dev)  
**Aprobador:** Jelkin (CEO)  
**Estado:** Borrador — pendiente aprobación

---

## 1. RESUMEN EJECUTIVO

Módulo de Inteligencia Artificial que asigna un puntaje de riesgo (score) a cada reporte anónimo recibido, basándose en el texto de la descripción y, opcionalmente, en evidencias textuales. El objetivo es priorizar la atención humana: reportes con score alto requieren revisión prioritaria por parte de las autoridades competentes.

El modelo **no decide**, solo asiste. Todo score es una probabilidad con explicabilidad (SHAP) y debe ser validado por un humano antes de cualquier acción institucional.

---

## 2. ALCANCE

### 2.1 Dentro del alcance
- Endpoint `/api/analyze/{report_id}` para calcular score de riesgo de un reporte existente.
- Modelo de clasificación/scoring entrenado con texto de descripciones.
- Almacenamiento del score, nivel de riesgo y versión del modelo en la base de datos.
- Explicabilidad básica: palabras/frases que más influyeron en el score.
- Registro de auditoría de cada predicción (model_version, score, timestamp).
- Tests unitarios del modelo, tests de integración del endpoint, tests de red-teaming.
- Dataset de entrenamiento inicial sintético y etiquetado (desarrollo únicamente).

### 2.2 Fuera del alcance
- Notificación automática a autoridades.
- Toma de decisiones automatizada sobre menores de edad.
- Análisis de imágenes (evidencia tipo `image`) en esta versión.
- Entrenamiento continuo con datos de producción sin anonimización y consentimiento explícito.
- Panel de administración para revisar reportes (módulo futuro).

---

## 3. USER STORIES

### US-004: Priorizar reportes por riesgo
**Como** autoridad revisora  
**Quiero** que el sistema clasifique reportes por nivel de riesgo  
**Para** atender primero los casos más urgentes

**Criterios de aceptación:**
- Given un reporte con descripción detallada
- When se ejecuta el análisis
- Then el sistema devuelve un score entre 0 y 1 y un nivel `low|medium|high|critical`

**Prioridad:** Alta  
**Estimación:** 13h

### US-005: Entender por qué un reporte tiene score alto
**Como** autoridad revisora  
**Quiero** ver qué palabras o frases influyeron en el score  
**Para** validar la recomendación del modelo

**Criterios de aceptación:**
- Given un reporte analizado
- When consulto el resultado
- Then recibo una lista de tokens/segmentos con su contribución al score

**Prioridad:** Media  
**Estimación:** 8h

### US-006: Auditar decisiones del modelo
**Como** auditor del sistema  
**Quiero** conocer la versión del modelo y fecha de cada predicción  
**Para** rastrear la evolución del scoring

**Criterios de aceptación:**
- Given una predicción realizada
- Then queda registrado model_version, score, nivel y timestamp

**Prioridad:** Media  
**Estimación:** 5h

### US-007: Evitar sesgos y abusos del modelo
**Como** responsable ético  
**Quiero** que el modelo no discrimine por género, etnia o zona  
**Para** garantizar un uso justo

**Criterios de aceptación:**
- Given un dataset de validación balanceado
- When evalúo fairness
- Then no hay disparidad significativa entre grupos demográficos

**Prioridad:** Alta  
**Estimación:** 8h

### US-008: Proteger contra adversarial inputs
**Como** administrador del sistema  
**Quiero** que el modelo sea robusto ante textos diseñados para engañarlo  
**Para** evitar manipulación del scoring

**Criterios de aceptación:**
- Given textos con evasión, negación o distracción
- When el modelo predice
- Then el score no se ve manipulado artificialmente a bajo riesgo

**Prioridad:** Media  
**Estimación:** 8h

---

## 4. REQUISITOS FUNCIONALES

| ID | Requisito | User Story | Prioridad | Estado |
|----|-----------|------------|-----------|--------|
| RF-006 | Calcular score de riesgo para un reporte | US-004 | Alta | Pendiente |
| RF-007 | Clasificar en niveles low/medium/high/critical | US-004 | Alta | Pendiente |
| RF-008 | Explicar contribución de tokens con SHAP | US-005 | Media | Pendiente |
| RF-009 | Registrar versión del modelo y timestamp | US-006 | Media | Pendiente |
| RF-010 | Ejecutar análisis de forma asíncrona opcional | US-004 | Baja | Pendiente |
| RF-011 | Endpoint de health del modelo | US-004 | Media | Pendiente |
| RF-012 | Permitir reentrenamiento offline con dataset versionado | US-007 | Media | Pendiente |

---

## 5. REQUISITOS NO FUNCIONALES

| ID | Requisito | Categoría | Criterio | Prioridad |
|----|-----------|-----------|----------|-----------|
| RNF-006 | Latencia < 500ms por predicción | Performance | 95 percentile | Alta |
| RNF-007 | AUC-ROC ≥ 0.80 en dataset de test | Calidad IA | Validación holdout | Alta |
| RNF-008 | Explicabilidad disponible para score > 0.7 | Transparencia | SHAP values | Alta |
| RNF-009 | Modelo versionado y reproducible | MLOps | Random seed fijado, artefactos versionados | Alta |
| RNF-010 | Sin datos identificables en logs de IA | Privacidad | No se registra texto original | Alta |
| RNF-011 | Fairness auditado antes de deploy | Ética | Disparidad < 10% entre grupos | Alta |
| RNF-012 | Cobertura de tests ≥ 80% | Calidad | pytest + vitest | Alta |

---

## 6. REGLAS DE NEGOCIO

- RN-005: El score es una probabilidad entre 0.0 y 1.0.
- RN-006: Niveles de riesgo:
  - `low`: score < 0.40
  - `medium`: 0.40 ≤ score < 0.65
  - `high`: 0.65 ≤ score < 0.85
  - `critical`: score ≥ 0.85
- RN-007: Todo reporte con nivel `critical` requiere revisión humana prioritaria.
- RN-008: El modelo no debe entrenarse con datos de producción sin anonimización y aprobación explícita.
- RN-009: Las explicaciones no deben incluir datos personales ni identificadores del reportante.
- RN-010: El sistema debe poder operar sin el componente IA (fallback a no score).

---

## 7. DATOS

### 7.1 Dataset de entrenamiento inicial
- **Origen:** Sintético generado por ODIN para desarrollo.
- **Tamaño mínimo:** 1.500 ejemplos balanceados.
- **Etiqueta:** `risk_score` continuo o `is_high_risk` binario.
- **Features:** texto de la descripción del reporte.
- **Restricciones:** No contiene nombres reales, direcciones ni datos identificables.
- **Ubicación:** `src/ia/data/synthetic_train_v1.csv` (etiquetado como sintético).

### 7.2 Datos de producción
- **Uso:** Solo para inferencia, nunca para entrenamiento sin consentimiento/anonimización.
- **Almacenamiento:** Texto encriptado en la tabla `reports` (existente).

---

## 8. MOCKUPS / WIREFRAMES

No aplica para el componente backend. La UI de visualización del score queda para el panel de administración (módulo futuro).

El endpoint devolverá:

```json
{
  "report_id": "uuid",
  "score": 0.87,
  "level": "critical",
  "model_version": "risk-v1.0.0",
  "timestamp": "2026-06-13T00:00:00Z",
  "explanation": [
    {"token": "menor", "contribution": 0.12},
    {"token": "desprotegido", "contribution": 0.09}
  ]
}
```

---

## 9. CRITERIOS DE ACEPTACIÓN GLOBALES

- [ ] Dataset sintético etiquetado y versionado en `src/ia/data/`.
- [ ] Modelo entrenado con AUC-ROC ≥ 0.80 en test.
- [ ] Endpoint `/api/analyze/{report_id}` funcional y testeado.
- [ ] Explicabilidad SHAP integrada.
- [ ] Tabla/entidad `Analysis` almacena score, nivel, versión y timestamp.
- [ ] Tests de red-teaming documentados.
- [ ] Reporte de fairness sin disparidades críticas.
- [ ] Cobertura backend ≥ 80%.
- [ ] ADR-IA-001 aprobado.
- [ ] Jelkin aprueba spec, plan y tasks.

---

> Generado por ODIN — Innovadataco
