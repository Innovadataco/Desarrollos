# ADR-002 — PWA vs App Store

**Proyecto:** Semáforo de Confianza (005)  
**Código:** IDC_2026_05  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  
**Estado:** ✅ Aprobado

---

## Contexto

El producto pivoteó de "plataforma de reporte anónimo" a "buscador universal de confianza + reporte anónimo". La decisión de frontend (PWA vs App Store nativo) es crítica para anonimato, velocidad de desarrollo, y adopción en LATAM.

## Decisión

**Usar PWA (Progressive Web App) en lugar de aplicaciones nativas iOS/Android.**

## Alternativas Consideradas

| Alternativa | Pros | Contras | Decisión |
|-------------|------|---------|----------|
| PWA (React + Vite + Workbox) | Sin fricción, sin tracking, sin tienda, velocidad de deploy, costo $0, anonimato perfecto | Sin notificaciones push en iOS (limitadas), sin acceso a cámara en background | ✅ Elegido |
| React Native | Casi nativo, un solo codebase, notificaciones push | Requiere App Store/Play Store, metadata de dispositivo, SDKs de tracking, revisiones de tienda | ❌ Rechazado |
| Flutter | Rápido, nativo, UI consistente | Requiere App Store/Play Store, SDKs de tracking, revisiones de tienda | ❌ Rechazado |
| App Store nativo (Swift/Kotlin) | Máximo rendimiento, acceso a hardware completo | Costo de licencia ($99/año Apple + $25 Google), revisiones 3-5 días, comisiones 30%, metadata de dispositivo | ❌ Rechazado |
| Web normal (sin PWA) | Más simple | Sin instalación, sin cache, sin offline, mala UX en móvil | ❌ Rechazado |

## Análisis de Anonimato

| Dato | PWA | App Store |
|------|-----|-----------|
| IP | Controlado (nginx log off) | Controlado |
| User-Agent | Controlado | Controlado |
| Device ID | ❌ No existe | ❌ No en web, pero SDKs pueden leer |
| IDFA/GAID | ❌ No existe | ✅ Sí (si se usa SDK de analytics) |
| Install metadata | ❌ No existe | ✅ Sí (tienda sabe quién instaló) |
| Push token | ⚠️ Limitado (iOS no permite web push) | ✅ Sí |
| Camera access | ✅ Sí (con permiso explícito) | ✅ Sí (con permiso explícito) |
| Geolocation | ⚠️ Solo si consiente | ⚠️ Solo si consiente |
| Cookies | ❌ No usamos | ❌ No usamos |
| localStorage | ⚠️ Solo si consiente (premium) | ⚠️ Solo si consiente |

**Conclusión:** PWA elimina toda la metadata de instalación y tracking de tienda. Es el único vector que no podemos controlar en App Store.

## Consecuencias

### Positivas
- Anonimato perfecto: sin metadata de instalación, sin SDKs de tienda, sin IDFA
- Velocidad: deploy en minutos, no días de revisión de tienda
- Costo: $0 de licencia, $0 de comisiones
- Acceso universal: cualquier navegador, cualquier dispositivo, cualquier país
- Latinoamérica: la mayoría de usuarios no usa App Store; usan WhatsApp Web y navegador móvil
- Privacidad: sin dependencias de frameworks de tracking

### Negativas
- iOS no soporta web push notifications (limitado en 2026, posible cambio en iOS 17+)
- iOS no soporta add to home screen automático (requiere instrucciones manuales)
- Sin acceso a contactos del teléfono (irrelevante para este producto)
- Offline: cache con Workbox, pero no tan robusto como app nativa
- Performance: ligeramente inferior a nativo (aceptable para formularios simples)

## Mitigaciones

| Limitación | Mitigación |
|------------|------------|
| No push en iOS | Usar SMS/email para alertas premium (no push) |
| No add-to-home automático | Instrucciones visuales en onboarding ("Añadir a inicio") |
| Offline limitado | Workbox con cache de shell + datos |
| Performance | React 19 + Vite + lazy loading + code splitting |

## Stack PWA

| Capa | Tecnología |
|------|------------|
| Framework | React 19 |
| Bundler | Vite |
| CSS | Tailwind CSS |
| PWA | vite-plugin-pwa + Workbox |
| Service Worker | Precache shell, runtime cache API |
| Manifest | manifest.json (icons, theme, start_url) |
| Offline | Workbox strategies: CacheFirst (shell), NetworkFirst (API) |
| Camera | navigator.mediaDevices.getUserMedia() |
| Upload | XMLHttpRequest / fetch con FormData |

## Notas

- MVP: PWA 100% del tráfico
- Futuro: si escala a >10,000 usuarios activos, evaluar wrapper Capacitor o Tauri para PWA nativo
- No se descarta App Store para futuro, pero requiere análisis legal de metadata de tienda
- Testing: Playwright E2E en viewport móvil (320px, 375px, 414px)

---

> *ADR generado por ZEUS — Innovadataco*  
> *Módulo 002 — PWA vs App Store*
