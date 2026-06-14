# ADR-005 — Integración con Autoridades

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ Pendiente aprobación

---

## Contexto

El sistema debe enviar alertas estructuradas a autoridades colombianas (ICBF, Fiscalía, Policía) y estándares internacionales (NCMEC). La decisión crítica es: ¿cómo enviamos los datos sin exponer al reportante, sin asumir responsabilidad legal, y sin depender de APIs que no existen?

## Decisión

**Usar un modelo híbrido: email estructurado como fallback universal + API gateway propio para instituciones que firmen contrato + integración NCMEC para estándar internacional.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| Email estructurado (JSON attachment) | Universal, funciona con cualquier institución, sin dependencia de API | Menos automatizado, requiere parsing manual por la institución | ✅ Elegido (fallback) |
| API gateway propio (REST + API key) | Automatizado, controlado, auditable, escalable | Requiere que la institución tenga capacidad técnica | ✅ Elegido (primario) |
| Webhook (institución expone endpoint) | Push inmediato, sin polling | Requiere que la institución exponga endpoint seguro, raro en gobierno | ⚠️ Futuro |
| Portal web (institución accede a dashboard) | Simple, sin integración técnica | Requiere que alguien revise manualmente, latencia alta | ✅ Elegido (panel admin) |
| Integración directa con sistema de ICBF | Máxima integración, ideal | ICBF no tiene API pública, proceso de integración puede tomar 6-12 meses | ⚠️ Futuro |
| NCMEC CyberTipline API | Estándar internacional, reconocido | Solo para reportes internacionales, requiere registro | ✅ Elegido (internacional) |

## Arquitectura de Pasarela

```
┌─────────────────────────────────────────────────────────────┐
│                    PANEL ADMIN (Innovadataco)              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│
│  │ Alerta      │  │ Digest      │  │ Configuración       ││
│  │ Manual      │  │ Automático  │  │ Umbrales            ││
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘│
└─────────┼────────────────┼────────────────────────────────┘
          │                │
          ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                   API GATEWAY (FastAPI)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│
│  │ Auth        │  │ Rate Limit  │  │ Format Transform    ││
│  │ API Key     │  │ 100/hr/inst │  │ JSON → PDF → NCMEC  ││
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘│
└─────────┼────────────────┼────────────────────────────────┘
          │                │
          ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │  ICBF   │      │ Fiscalía│      │ Policía │
    │  Email  │      │  Email  │      │  Email  │
    │  API*   │      │  API*   │      │  API*   │
    └─────────┘      └─────────┘      └─────────┘
          │                │                │
          ▼                ▼                ▼
    ┌─────────────────────────────────────────┐
    │           NCMEC (Internacional)         │
    │         CyberTipline API v2             │
    └─────────────────────────────────────────┘
```

*API = API gateway propio si la institución firma contrato y tiene capacidad técnica.

## Formatos de Exportación

### 1. JSON Estructurado (estándar interno)

```json
{
  "schema_version": "1.0",
  "report_hash": "SHA256-64CHAR",
  "reported_at": "2026-06-13T10:00:00Z",
  "category": "grooming",
  "score": 0.87,
  "level": "severe",
  "identifier_type": "phone",
  "identifier_normalized": "+573001234567",
  "identifier_hash": "SHA256",
  "city": "Bogotá",
  "country": "Colombia",
  "evidence_types": ["image"],
  "description_summary": "Resumen de 200 chars generado por IA...",
  "analysis": {
    "model_version": "grooming-v1.0",
    "grooming_indicators": ["secrecion", "aislamiento"],
    "confidence": 0.92
  },
  "profile": {
    "report_count": 7,
    "score_average": 0.78,
    "is_network": false
  }
}
```

**Nota:** Nunca incluye texto original del reporte, identificador real del reportante, ni coordenadas exactas.

### 2. PDF Institucional

- Portada con logo Innovadataco, fecha, número de reporte
- Resumen ejecutivo (1 página)
- Detalle del reporte (agregado, no identificable)
- Análisis de IA (score, categoría, indicadores)
- Perfil del identificador (si aplica)
- Evidencia: thumbnails con marca de agua
- Pie de página legal: "Innovadataco es canal tecnológico. La investigación judicial es responsabilidad exclusiva de las autoridades competentes."

### 3. NCMEC CyberTipline v2

```xml
<report xmlns="http://www.missingkids.org/ncmec">
  <incident>
    <type>online_enticement</type>
    <reporter>
      <type>anonymous</type>
    </reporter>
    <subject>
      <identifier type="phone">+573001234567</identifier>
    </subject>
    <summary>Resumen de 200 chars...</summary>
  </incident>
</report>
```

## Seguridad

| Aspecto | Medida |
|---------|--------|
| Autenticación | API key por institución (bcrypt), rotada cada 3 meses |
| Rate limiting | 100 requests/hour por institución |
| TLS | TLS 1.3 obligatorio para API gateway |
| Audit trail | Cada request registrado en AuditLog |
| Sin datos identificables | Nunca retorna texto original, identificador real del reportante, ni coordenadas |
| Confirmación | Institución debe confirmar recepción (POST /api/gateway/v1/confirm) |
| Retry | 3 intentos con backoff exponencial si falla entrega |

## Modelo de Negocio

- **Piloto:** Innovadataco ofrece 3 meses gratis (sin costo de licencia) para construir credibilidad
- **Contrato:** Licencia anual + soporte técnico. Innovadataco NO opera el sistema, solo provee tecnología.
- **Responsabilidad legal:** Definida en contrato. Innovadataco es canal tecnológico, no operador de respuesta.

## Notas

- La integración con ICBF requiere contacto formal con Dirección de Innovación o Tecnología
- La Fiscalía puede requerir formato específico de denuncia (ajustar PDF según requerimiento)
- La Policía (GAULA/Grupo Infancia) puede preferir email estructurado a API
- NCMEC requiere registro previo y aprobación de la plataforma
- Todo contacto institucional debe ser documentado en CRM de Innovadataco

---

> *ADR generado por ZEUS — Innovadataco*  
> *Módulo 006 — Pasarela Institucional*
