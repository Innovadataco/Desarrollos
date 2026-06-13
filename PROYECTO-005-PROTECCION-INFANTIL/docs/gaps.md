# Gaps — Resueltos y Pendientes

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 2.0  

---

## Gaps Resueltos (v1.0 → v2.0)

| ID | Gap | Resolución | Módulo |
|----|-----|------------|--------|
| G-001 | Falta de visión de producto clara | Pivote a "Semáforo de Confianza" + buscador universal + modelo freemium B2C + B2B2C | 002 |
| G-002 | Sin monetización definida | Freemium B2C ($2.99/mes) + B2B2C colegios ($1,000/año) | 002, 006 |
| G-003 | Sin evidencia multimedia | Imágenes, videos, audios, capturas con encriptación AES-256-GCM + strip EXIF | 001 |
| G-004 | Sin categorización de reportes | 6 categorías (CAT-01 a CAT-06) para entrenamiento de IA | 001 |
| G-005 | Sin validación de contactos previos | Buscador universal: consulta si identificador tiene reportes + semáforo | 002 |
| G-006 | Sin IA para clasificación | NLP ensemble (LR + RF) para scoring, categorización, detección grooming | 003 |
| G-007 | Sin clustering geográfico | MaxMind GeoLite2 local + detección de red organizada (≥3 ciudades/países) | 004 |
| G-008 | Sin perfil de agresor | Tabla consolidada por identificador: timeline, scores, ciudades, evidencia | 004 |
| G-009 | Sin panel de admin seguro | Auth JWT + roles + 2FA + desencriptación bajo demanda + audit trail | 005 |
| G-010 | Sin integración con autoridades | API gateway + email estructurado + NCMEC + pasarela institucional | 006 |
| G-011 | Sin modelo de negocio B2B2C | Plan para colegios y distritos educativos con panel institucional | 002, 006 |
| G-012 | PWA vs App Store no decidido | Decisión: PWA (anonimato perfecto, sin tienda, sin tracking) | 002 |
| G-013 | Sin explicabilidad IA | SHAP values para scores > 0.7, model card, fairness audit | 003 |
| G-014 | Sin red-teaming IA | 0 falsos negativos de alto riesgo, disparidad < 10% entre subgrupos | 003 |
| G-015 | Sin pasarela API para instituciones | API gateway con API key, rate limiting, formato JSON/PDF/NCMEC | 006 |

---

## Gaps Pendientes (v2.0)

| ID | Gap | Impacto | Plan de Resolución | Módulo | Fecha |
|----|-----|---------|-------------------|--------|-------|
| G-016 | Dataset real de entrenamiento (reportes reales) | Alto | Acumular 500 reportes con consentimiento para uso en ML, o comprar dataset anónimo | 003 | Dic 2026 |
| G-017 | Contrato con ICBF/Fiscalía/Policía | Alto | Contacto formal + demo + piloto gratuito 3 meses | 006 | Sep-Oct 2026 |
| G-018 | HSM (Hardware Security Module) para KEK | Medio | Evaluar AWS CloudHSM o YubiHSM para rotación automática de claves | 001 | 2027 |
| G-019 | Auditoría de seguridad externa (OWASP ZAP + pentest) | Alto | Contratar firma de seguridad para pentest antes de producción | Todos | Nov 2026 |
| G-020 | Seguro de responsabilidad civil | Alto | Contratar seguro si Innovadataco opera bajo Modelo B | Negocio | Dic 2026 |
| G-021 | Notificaciones push (iOS) | Medio | iOS no soporta web push. Evaluar SMS/email para alertas premium | 002 | 2027 |
| G-022 | Embeddings BERT/RoBERTa para IA | Medio | Mejorar precisión cuando haya dataset > 10,000 ejemplos | 003 | 2027 |
| G-023 | API webhook para instituciones (push) | Medio | Si institución tiene capacidad técnica, ofrecer webhook además de email | 006 | 2027 |
| G-024 | Multi-idioma (portugués, inglés) | Bajo | LATAM: Brasil, México. i18n estructura preparada | Todos | 2027 |
| G-025 | App nativa iOS/Android (futuro) | Bajo | Si escala a >100,000 usuarios, evaluar wrapper Capacitor o Tauri | 002 | 2027 |
| G-026 | Integración directa con sistema de ICBF | Bajo | Requiere proceso formal de integración tecnológica (6-12 meses) | 006 | 2027 |
| G-027 | Machine learning en evidencia multimedia (detección de CSAM) | Medio | No en MVP. Requiere modelo de detección de material de abuso infantil, con riesgo legal y ético. | 003 | 2027 |

---

## Gaps Cerrados (No Relevantes)

| ID | Gap | Razón de Cierre |
|----|-----|-----------------|
| G-028 | Scoring de pedofilia (número 0-100) | Cerrado. Legalmente conservador: nunca acusar, solo "semáforo de confianza comunitaria" |
| G-029 | Evidencia pública (mostrar reportes) | Cerrado. Privacidad absoluta: nunca exponer contenido de reportes |
| G-030 | Alertar al agresor | Cerrado. Legalmente prohibido: nunca notificar al identificador reportado |

---

> *Documento generado por ZEUS — Innovadataco*  
> *Versión 2.0 — Gaps resueltos y nuevos identificados*
