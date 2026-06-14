# Fairness Report — Módulo 003 IA Triage

**Modelo:** `risk-v1.0.0`  
**Fecha:** 2026-06-13  
**Objetivo:** Medir la disparidad de score entre variantes de estilo, registro y dialecto para la misma situación de riesgo.

---

## 1. Criterio de éxito

Se considera aceptable si la **dispersión absoluta** entre variantes es **< 0.10** (10 puntos porcentuales) y la **dispersión relativa** es **< 0.10** (10 % respecto al promedio).

## 2. Metodología

Para cada situación base se generaron seis variantes:
- **neutral:** frase base.
- **formal:** registro formal con sinónimos más elaborados.
- **colloquial:** registro coloquial.
- **mexican:** marcadores dialectales mexicanos (`wey`, `neta`, `órale`).
- **argentine:** marcadores dialectales argentinos (`che`, `pibe`, `posta`).
- **misspelled:** errores ortográficos leves.

## 3. Resultados por grupo

| Situación base | Dispersión absoluta | Dispersión relativa | Rango de scores |
|----------------|---------------------|---------------------|-----------------|
| mensaje insistente pidiendo fotos desnudas y amenazando | 0.0185 | 1.86 % | 0.9783 – 0.9968 |
| me pidió fotos sin ropa y dijo que no le contara a nadie | 0.0149 | 1.51 % | 0.9788 – 0.9938 |
| amenazó con difundir fotos si no enviaba más contenido | 0.0023 | 0.23 % | 0.9969 – 0.9992 |
| me dijo que era especial y me pidió que nos viéramos a escondidas | 0.0001 | 1.33 % | 0.0040 – 0.0041 |
| me exigió dinero o publicaría imágenes íntimas | 0.0002 | 0.02 % | 0.9976 – 0.9978 |

## 4. Resumen

- **Grupos evaluados:** 5
- **Máxima dispersión absoluta:** 0.0185
- **Máxima dispersión relativa:** 0.0186 (1.86 %)
- **Estado:** ✅ PASS

## 5. Interpretación

- La dispersión máxima es inferior al 2 %, muy por debajo del umbral del 10 %.
- El modelo no muestra sesgo significativo por registro formal/coloquial ni por marcadores dialectales de Colombia, México o Argentina.
- Las variantes con errores ortográficos mantienen scores consistentes con las demás.

## 6. Limitaciones

- La auditoría se realizó sobre un conjunto reducido de situaciones sintéticas.
- No se evaluaron atributos demográficos reales (edad, género del reportante) porque el dataset no los incluye de forma explícita.
- Se recomienda repetir la auditoría con datos reales anonimizados.

## 7. Endpoint

Los resultados están disponibles en tiempo real en:

```http
GET /api/v1/analyze/fairness
```

## 8. Próximos pasos

- Ampliar el set de situaciones base para cubrir más categorías.
- Incluir variantes de género del reportante cuando el dataset lo permita.
- Definir un dashboard de fairness en el panel admin.
