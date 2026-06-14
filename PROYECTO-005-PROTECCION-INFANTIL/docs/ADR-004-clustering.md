# ADR-004 — Clustering Geográfico y Privacidad

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.1  
**Autor:** ZEUS / ODIN  
**Estado:** ✅ Aprobado

---

## Contexto

El sistema necesita detectar si un mismo identificador (teléfono, email, cuenta) ha sido reportado desde múltiples ciudades o países, lo cual indica una posible red organizada de explotación infantil. Esto requiere geocodificación de la ubicación del reportante, pero sin exponer su identidad ni ubicación exacta.

## Decisión

**Usar geocodificación aproximada (ciudad/país) con consentimiento explícito del usuario, basada en IP usando MaxMind GeoLite2 local (sin API externa), almacenando solo ciudad y país, nunca coordenadas exactas ni IP.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| IP → GeoLite2 local | Gratuito, local, sin API externa, precisión a nivel ciudad | Requiere actualización de base de datos, no 100% preciso | ✅ Elegido |
| IP → API externa (ip-api, ipinfo) | Más preciso, sin mantenimiento de BD | Dependencia de terceros, latencia, costo, privacidad de IP | ❌ Rechazado |
| GPS del navegador | Preciso, voluntario | Coordenadas exactas = riesgo de tracking del reportante | ❌ Rechazado |
| Sin geocodificación | Máximo anonimato | No se puede detectar redes organizadas | ❌ Rechazado |
| Geocodificación sin consentimiento | Más datos para clustering | Violación de privacidad, posible ilegal en algunos países | ❌ Rechazado |

## Consecuencias

### Positivas
- Privacidad: solo ciudad/país, nunca coordenadas exactas
- Local: GeoLite2 se descarga, no hay API externa que vea IPs
- Consentimiento: usuario explícito "Compartir ciudad aproximada"
- Detección: puede identificar redes organizadas (mismo ID desde 3+ ciudades)
- Cache Redis de perfiles y redes reduce carga de PostgreSQL

### Negativas
- GeoLite2 no es 100% preciso (ciudad puede estar mal en móvil, VPN)
- Requiere actualización mensual de la base de datos
- Si usuario no consiente, el reporte no contribuye al clustering (aceptable)

## Implementación

El servicio `app/services/geoip_service.py` encapsula la resolución:

```python
from app.services.geoip_service import get_location_from_ip

city, country = get_location_from_ip(client_ip, request, consent=True)
```

Reglas:

1. Si `consent=False` retorna `(None, None)`.
2. La IP se hashea con SHA-256 y se descarta inmediatamente.
3. Si existe `data/GeoLite2-City.mmdb` (o la ruta configurada en `GEOLITE2_PATH`), se usa GeoLite2.
4. Si GeoLite2 no está disponible, se usan las cabeceras `X-Client-City` y `X-Client-Country`.
5. Solo se retorna ciudad/país. Coordenadas, códigos postales, etc. nunca se consultan ni almacenan.

El `reportes.py` utiliza este servicio cuando `consent_location=True`:

```python
city, country = _extract_location(request, consent=bool(payload.consent_location))
```

## Almacenamiento

| Dato | ¿Almacenado? | Nota |
|------|-------------|------|
| IP original | ❌ NO | Hasheada y descartada inmediatamente |
| IP hash | ⚠️ Solo en Redis | Para rate limiting, TTL 1h |
| Coordenadas GPS | ❌ NO | Nunca |
| Ciudad aproximada | ✅ SÍ | En `Report.city`, solo si `consent=True` |
| País | ✅ SÍ | En `Report.country`, solo si `consent=True` |
| Barrio/Zona | ❌ NO | Nunca |
| Código postal | ❌ NO | Nunca |

## Algoritmo de Red Organizada

Se requieren 2 o más criterios para marcar `is_network = true`:

```python
def is_network(profile: Profile) -> bool:
    criterios = 0
    
    if profile.cities_count >= 3:
        criterios += 1
    if profile.countries_count >= 2:
        criterios += 1
    if profile.report_count >= 5 and profile.score_average > 0.6:
        criterios += 1
    if len(profile.evidence_types) >= 3:
        criterios += 1
    
    return criterios >= 2
```

## Caché

| Clave | TTL | Uso |
|-------|-----|-----|
| `profile:{hash}` | 1h | Perfil serializado |
| `networks:list` | 15 min | Lista de perfiles con `is_network=true` |

La cache se invalida automáticamente al recalcular un perfil (`profile_service.update_profile_from_report`).

## Notas

- GeoLite2 se actualiza mensualmente (cron job: primer lunes de mes).
- Si GeoLite2 no está disponible, el sistema continúa operando con cabeceras (graceful degradation).
- El consentimiento es explícito: checkbox "Compartir mi ciudad aproximada para detectar redes organizadas" (no pre-marcado).
- El checkbox puede ser desactivado sin afectar el envío del reporte (solo afecta clustering).
- Para reportes sin geocodificación, el score individual sigue siendo válido para alertas.

---

> *ADR generado por ZEUS — Innovadataco*  
> *Módulo 004 — Clustering Geográfico*
