# Lecciones Aprendidas — Proyecto 005

## 1. Stack y entorno

- Python 3.14.5 local funciona bien con FastAPI 0.136.3 y SQLAlchemy 2.0.50.
- El Dockerfile base debe alinearse a la versión local (3.14) para evitar sorpresas de sintaxis/dependencias.
- El rate limiting con `limits` requiere Redis en producción; el fallback en memoria es suficiente para tests y demo.

## 2. Seguridad y anonimato

- No almacenar IP, user-agent, cookies ni fingerprint es una restricción de negocio; validarla con tests de modelo evita regresiones.
- Encriptar con DEK por campo + KEK derivada de variable de entorno mantiene los datos en reposo seguros y permite rotación futura.
- El hash de identificador (SHA-256 canonizado) permite agrupar reportes sin revelar el identificador original.

## 3. Diseño UX

- En contextos de estrés, menos es más: wizard de 3 pasos, chips grandes, botón "Atrás" siempre visible.
- Los colores del semáforo deben comunicar nivel de riesgo sin alarmismo; rojo = acción, verde = alivio.
- El mensaje post-reporte debe validar la acción moral del usuario, no solo confirmar recepción técnica.

## 4. IA y scoring

- Un ensemble TF-IDF + Logistic Regression/Random Forest con calibración entrega buenos resultados (AUC-ROC 0.90, F1 0.88) con un dataset sintético pequeño.
- SHAP es clave para explicabilidad ante operadores y auditores.
- Red teaming simple (100 ejemplos adversariales) detectó 0 falsos negativos críticos en el modelo entrenado.

## 5. Integración institucional

- La pasarela debe soportar tanto API key como fallback por email estructurado.
- Nunca exponer datos encriptados por defecto; el modo "full" requiere justificación institucional y auditoría.

## 6. Pruebas

- Los tests de integración deben forzar variables de entorno antes de importar la app (conftest al inicio).
- El middleware `TrustedHostMiddleware` bloquea `testserver` si no se configura `ALLOWED_HOSTS` en pruebas.
- Actualizar los tests al nuevo UI/UX (wizard) evita falsos negativos en CI.

## 7. Deuda técnica pendiente

- Unificar volumen de Docker Compose con el path real del modelo IA.
- Revisar CORS y hosts permitidos en producción.
- Implementar export PDF/NCMEC cuando la pasarela lo requiera.
- Añadir análisis automático de reportes recibidos y generación de alertas/auditoría.
