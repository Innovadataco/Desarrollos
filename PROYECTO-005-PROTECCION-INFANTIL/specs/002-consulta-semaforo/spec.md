# SPEC-002 — Consulta Semáforo de Confianza (Módulo 002)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ NUEVO — Pendiente desarrollo

---

## 1. RESUMEN

El Módulo 002 es el **corazón del producto pivoteado**: un buscador universal donde cualquier persona puede consultar si un número de teléfono, cuenta de redes sociales, email o URL ha sido reportado como riesgo para menores. El sistema retorna un **Semáforo de Confianza Comunitaria** con estadísticas agregadas, sin exponer información identificable del reportante ni detalles del contenido.

---

## 2. FLUJO DE USUARIO

```
[Usuario abre PWA → Tapa "Consultar"]
           │
           ▼
[Ingresa identificador: +573001234567, @usuario, email, URL]
           │
           ▼
[Sistema consulta en base de datos encriptada]
           │
           ▼
[Resultado: Semáforo de Confianza]
           │
           ├── 🟢 VERDE — Sin reportes. Sin señales.
           ├── 🟡 AMARILLO — 1-2 reportes leves. Precaución.
           ├── 🔴 ROJO — 3+ reportes o patrones de riesgo. Alerta.
           └── ⚫ NEGRO — Red organizada detectada. Riesgo crítico.
           │
           ▼
[Detalle: "Este identificador tiene X reportes de contacto inapropiado con menores."]
[Acción: "Reportar" → lleva a Módulo 001]
```

---

## 3. ENDPOINTS

### `GET /api/validate/{identifier}`

**Parámetros:**
```
identifier: string (teléfono, email, @usuario, URL)
```

**Response 200 — Sin reportes (🟢):**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "semaforo": "verde",
  "report_count": 0,
  "score_average": null,
  "score_max": null,
  "first_reported_at": null,
  "last_reported_at": null,
  "message": "Sin reportes registrados. El semáforo está verde.",
  "report_button": true
}
```

**Response 200 — Con reportes (🟡/🔴/⚫):**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "semaforo": "rojo",
  "report_count": 7,
  "score_average": 0.78,
  "score_max": 0.95,
  "first_reported_at": "2026-04-15",
  "last_reported_at": "2026-06-10",
  "categories": ["grooming", "solicitud_material"],
  "cities_count": 4,
  "countries_count": 2,
  "is_network": true,
  "message": "Este identificador tiene 7 reportes de contacto inapropiado con menores, detectado desde 4 ciudades y 2 países. Posible red organizada.",
  "report_button": true
}
```

**Response 429:**
```json
{
  "error": "Demasiadas consultas. Espere 1 hora.",
  "retry_after": 3600
}
```

---

## 4. ALGORITMO DEL SEMÁFORO

```python
def calcular_semaforo(report_count, score_max, cities_count, is_network):
    if is_network:
        return "negro"  # Red organizada detectada
    if report_count >= 3 or score_max >= 0.8:
        return "rojo"   # Alerta
    if report_count >= 1 or score_max >= 0.5:
        return "amarillo"  # Precaución
    return "verde"  # Sin reportes
```

**Reglas:**
- `negro`: `is_network = True` (≥3 ciudades/países, mismo identificador)
- `rojo`: `report_count >= 3` OR `score_max >= 0.8`
- `amarillo`: `report_count >= 1` OR `score_max >= 0.5`
- `verde`: Sin reportes

---

## 5. BUSCADOR UNIVERSAL DE IDENTIFICADORES

El sistema acepta y normaliza múltiples tipos de identificadores:

| Tipo | Formato | Normalización | Ejemplo |
|------|---------|-------------|---------|
| Teléfono | +CCXXXXXXXXX | E.164, sin espacios | +573001234567 |
| Email | user@domain.com | Lowercase, sin espacios | juan@email.com |
| Usuario social | @usuario | Lowercase, sin @ | usuario123 |
| URL | https://... | Normalizar, quitar query params | https://site.com/perfil |
| Nombre de perfil | texto libre | Lowercase, trim | "juan carlos" → "juancarlos" |

**Hash de identificador:** SHA-256 del identificador normalizado. Se usa para buscar reportes sin almacenar el identificador en texto plano.

---

## 6. PRIVACIDAD Y ANONIMATO EN LA CONSULTA

| Dato | ¿Expuesto? | Nota |
|------|-----------|------|
| Contenido del reporte | ❌ NO | Nunca se muestra texto del reporte |
| Identificador del reportante | ❌ NO | No existe en el sistema |
| Fecha exacta del reporte | ⚠️ Solo fecha | Hora truncada |
| Ciudad del reporte | ⚠️ Solo conteo | "Reportado desde 4 ciudades" |
| Categorías | ✅ Sí | Tipos de incidente agregados |
| Score | ✅ Sí | Promedio y máximo |

---

## 7. MODELO DE NEGOCIO FREEMIUM

| Plan | Consultas/día | Detalle | Precio |
|------|---------------|---------|--------|
| Gratuito | 3 | Semáforo + conteo básico | $0 |
| Premium | Ilimitadas | Historial, alertas, tendencias | $2.99/mes |

**Premium features:**
- Alertas por email cuando un identificador consultado cambia de semáforo
- Historial de consultas (almacenado localmente en PWA, no en servidor)
- Export de reportes propios (por hash de reporte)

---

## 8. CRITERIOS DE ACEPTACIÓN (DoD)

- [ ] Endpoint /api/validate/{identifier} funcional y documentado
- [ ] Normalización de identificadores correcta (teléfono, email, usuario, URL)
- [ ] Semáforo calcula correctamente según reglas definidas
- [ ] No expone información identificable del reportante
- [ ] Rate limiting funciona: 11ra consulta retorna 429
- [ ] Página de consulta funciona en móvil (320px+)
- [ ] Resultado muestra semáforo visual (colores claros)
- [ ] Botón "Reportar" lleva al formulario de Módulo 001
- [ ] Tests unitarios ≥ 80% cobertura
- [ ] Tests de integración con TestClient
- [ ] ADR-002 aprobado (PWA vs App Store)

---

> *SPEC generado por ZEUS — Innovadataco*  
> *Módulo 002 — Nuevo en v2.0 del producto*
