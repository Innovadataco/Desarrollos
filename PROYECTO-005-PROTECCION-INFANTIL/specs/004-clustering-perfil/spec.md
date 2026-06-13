# SPEC-004 — Clustering Geográfico y Perfil de Agresor (Módulo 004)

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ⬜ NUEVO — Pendiente desarrollo

---

## 1. RESUMEN

El Módulo 004 implementa clustering geográfico, generación de perfiles de agresor, y detección de redes organizadas. Analiza reportes por identificador para detectar si el mismo número/cuenta ha sido reportado desde múltiples ciudades o países, lo cual indica una posible red organizada de explotación infantil.

**El sistema NO acusa.** Genera un "perfil de contacto inapropiado con menores" con datos agregados. La investigación judicial es responsabilidad de las autoridades.

---

## 2. FUNCIONALIDADES

### 2.1 Clustering Geográfico

Para cada identificador reportado:
1. Agrega ciudades y países únicos de los reportes (solo si el usuario consintió ubicación)
2. Cuenta cuántas ciudades/países únicos
3. Si ≥ 3 ciudades o ≥ 2 países → flag `is_network = true`
4. Actualiza semáforo a ⚫ NEGRO

### 2.2 Perfil de Agresor (término legal: "Perfil de Contacto")

Tabla consolidada por identificador:
- Cantidad de reportes
- Promedio y máximo de scores
- Ciudades y países únicos
- Tipos de evidencia recibidos
- Timeline de reportes (mes/año)
- Categorías más frecuentes
- Flag de red organizada

### 2.3 Detección de Red Organizada

Criterios para flag `is_network`:
- ≥ 3 ciudades únicas (en el mismo país)
- ≥ 2 países únicos
- ≥ 5 reportes con score promedio > 0.6
- ≥ 3 tipos de evidencia diferentes (foto, video, audio, captura)

---

## 3. ENDPOINTS

### `GET /api/profile/{identifier_hash}`

**Solo para panel admin (autenticado).**

**Response 200:**
```json
{
  "identifier_hash": "SHA256-DE-IDENTIFICADOR",
  "report_count": 12,
  "score_average": 0.74,
  "score_max": 0.95,
  "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
  "countries": ["Colombia", "México"],
  "cities_count": 4,
  "countries_count": 2,
  "is_network": true,
  "evidence_types": ["image", "audio", "screenshot"],
  "categories": ["grooming", "solicitud_material", "cita_persona"],
  "first_reported": "2026-02-15",
  "last_reported": "2026-06-10",
  "timeline": [
    {"month": "2026-02", "count": 2, "score_avg": 0.65},
    {"month": "2026-03", "count": 3, "score_avg": 0.72},
    {"month": "2026-04", "count": 4, "score_avg": 0.78},
    {"month": "2026-05", "count": 2, "score_avg": 0.81},
    {"month": "2026-06", "count": 1, "score_avg": 0.85}
  ],
  "alert": "POSIBLE RED ORGANIZADA: 12 reportes desde 4 ciudades y 2 países."
}
```

### `GET /api/networks`

**Solo admin.** Lista todos los identificadores con `is_network = true`.

---

## 4. ALGORITMO DE CLUSTERING

```python
def detectar_red(profile):
    criterios = 0
    
    if profile.cities_count >= 3:
        criterios += 1
    if profile.countries_count >= 2:
        criterios += 1
    if profile.report_count >= 5 and profile.score_average > 0.6:
        criterios += 1
    if len(profile.evidence_types) >= 3:
        criterios += 1
    
    return criterios >= 2  # is_network = true si cumple 2+ criterios
```

### 4.1 Geocodificación

- **Fuente:** IP del reporte (solo si `consent_location = true`)
- **Precisión:** Ciudad/país aproximado, no coordenadas exactas
- **Servicio:** MaxMind GeoLite2 (local, sin API externa) o geocodificación offline
- **Privacidad:** No almacenar IP. Solo ciudad/país. IP se hashea y descarta inmediatamente.

### 4.2 Agregación

- Índice en `identifier_hash` (PostgreSQL B-tree)
- Query agregada: `GROUP BY identifier_hash`
- Caché en Redis: perfil expira en 1h, recalcula en background

---

## 5. MODELO DE DATOS

### Entidad `Profile`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| identifier_hash | String(64), unique | Hash SHA-256 del identificador |
| report_count | Integer | Cantidad de reportes |
| score_average | Float | Promedio de scores de análisis |
| score_max | Float | Score máximo alcanzado |
| cities | JSON | Lista de ciudades únicas |
| countries | JSON | Lista de países únicos |
| cities_count | Integer | Conteo de ciudades |
| countries_count | Integer | Conteo de países |
| is_network | Boolean | Flag de red organizada |
| evidence_types | JSON | Tipos de evidencia únicos |
| categories | JSON | Categorías más frecuentes |
| first_reported_at | Date | Primer reporte |
| last_reported_at | Date | Último reporte |
| timeline | JSON | Reportes por mes (count, score_avg) |
| updated_at | DateTime | Última actualización |

### Entidad `ProfileUpdate` (audit trail)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | PK |
| profile_id | UUID | FK → Profile |
| report_id | UUID | FK → Report (qué reporte causó el update) |
| old_score_avg | Float | Score anterior |
| new_score_avg | Float | Score nuevo |
| old_cities_count | Integer | Ciudades anterior |
| new_cities_count | Integer | Ciudades nuevo |
| triggered_network | Boolean | Este update activó is_network |
| created_at | DateTime | Timestamp |

---

## 6. PRIVACIDAD

| Dato | ¿En el perfil? | Nota |
|------|---------------|------|
| Identificador real | ❌ NO | Solo hash |
| Texto del reporte | ❌ NO | Solo score agregado |
| Ciudad exacta | ❌ NO | Solo ciudad aproximada |
| Coordenadas GPS | ❌ NO | Nunca |
| IP | ❌ NO | Hasheada y descartada |
| Timeline del reporte | ⚠️ Mes/año | Sin día exacto |
| Score | ✅ SÍ | Agregado |
| Categorías | ✅ SÍ | Frecuencias |
| Evidencia types | ✅ SÍ | Tipos, no contenido |

---

## 7. CRITERIOS DE ACEPTACIÓN (DoD)

- [ ] Endpoint GET /api/profile/{identifier_hash} funcional (solo admin)
- [ ] Endpoint GET /api/networks funcional (solo admin)
- [ ] Clustering detecta correctamente mismo ID desde ≥3 ciudades
- [ ] Perfil genera tabla completa y precisa
- [ ] Alerta de red organizada funciona automáticamente (criterios ≥2)
- [ ] Geocodificación sin exponer coordenadas exactas ni IPs
- [ ] Índice en identifier_hash para query rápida
- [ ] Cache Redis de perfiles (TTL 1h)
- [ ] ProfileUpdate guarda audit trail de cada cambio
- [ ] Tests unitarios ≥ 80% cobertura
- [ ] Tests de integración con TestClient
- [ ] ADR-004 aprobado (clustering + privacidad)

---

> *SPEC generado por ZEUS — Innovadataco*  
> *Módulo 004 — Nuevo en v2.0*
