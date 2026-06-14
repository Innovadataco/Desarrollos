# GUÍA DE DISEÑO UX CENTRADO EN EL USUARIO
## Plataforma: Semáforo de Confianza
### Versión 1.0 — Documento de Referencia para Desarrolladores

> **Audiencia:** Equipo de desarrollo de ODIN-CEO  
> **Propósito:** Cada decisión de UI/UX debe validarse contra este documento.  
> **Contexto:** PWA para padres de familia que buscan verificar contactos sospechosos y reportar de forma anónima.

---

## 1. PERFIL DE USUARIO (PERSONAS)

Las tres personas representan el 90% de los usuarios esperados. Cada flujo de la aplicación debe responder a sus necesidades emocionales y prácticas.

### 1.1 Persona 1: Ana — "La madre preocupada"

| Dimensión | Descripción |
|-----------|-------------|
| **Edad** | 38 años |
| **Contexto** | Encontró mensajes de texto extraños en el celular de su hijo de 12 años. No sabe si exagerar o si hay algo real. |
| **Motivación** | Proteger a su hijo sin crear un conflicto familiar innecesario. |
| **Miedo principal** | "Si pregunto directamente, mi hijo se enoja y cierra la comunicación." |
| **Objetivo** | Verificar si ese número de contacto tiene reportes previos antes de tomar una decisión. |
| **Nivel de urgencia** | **Alto** — Actúa en las primeras 2 horas tras el descubrimiento. |
| **Dispositivo** | Celular Android, conexión 4G, usa WhatsApp todo el día. |
| **Nivel de estrés** | 8/10. Puede estar llorando o temblando mientras usa la app. |
| **Frase clave** | "Solo quiero saber si debo preocuparme de verdad." |

**Implicaciones de diseño:**
- No pedir registro — Ana no tiene paciencia para formularios largos en este momento.
- Resultados claros: verde (alivio), amarillo (precaución), rojo (acción).
- Botón de ayuda visible siempre — puede no entender qué hacer con un resultado.

---

### 1.2 Persona 2: Carlos — "El padre proactivo"

| Dimensión | Descripción |
|-----------|-------------|
| **Edad** | 45 años |
| **Contexto** | Su hija de 14 años mencionó un "nuevo amigo" que conoció en Discord. Carlos quiere verificar el número antes de que la situación avance. |
| **Motivación** | Prevenir problemas antes de que ocurran. Prefiere datos sobre intuiciones. |
| **Miedo principal** | "Si parezco desconfiado, mi hija deja de contarme cosas." |
| **Objetivo** | Verificar de forma privada, sin que su hija se entere. |
| **Nivel de urgencia** | **Medio-Alto** — Actúa en 24-48 horas, en un momento de calma. |
| **Dispositivo** | iPhone, usa Safari, tiene 2FA en todas sus cuentas. |
| **Nivel de estrés** | 5/10. Preocupado pero metódico. |
| **Frase clave** | "Prefiero saber ahora que lamentar después." |

**Implicaciones de diseño:**
- Búsqueda rápida y discreta: no guardar historial sin permiso.
- Resultados con contexto: si está verde, mostrar cuándo se verificó por última vez.
- Opción de compartir resultado en formato privado (PDF, imagen).

---

### 1.3 Persona 3: María — "La tía que cuida"

| Dimensión | Descripción |
|-----------|-------------|
| **Edad** | 52 años |
| **Contexto** | Cuida a sus sobrinos los fines de semana. Un desconocido se acercó a uno de ellos en el parque y le dio un número de contacto. |
| **Motivación** | Reportar el incidente para que otros padres estén informados. |
| **Miedo principal** | "No quiero que piensen que soy alarmista, pero esto no me pareció normal." |
| **Objetivo** | Reportar de forma anónima, sin que la situación se convierta en un proceso legal complicado. |
| **Nivel de urgencia** | **Medio** — Actúa en 24-72 horas, cuando tiene un momento libre. |
| **Dispositivo** | Celular básico, pantalla pequeña, visión no perfecta. |
| **Nivel de estrés** | 6/10. Quiere ayudar pero no verse involucrada. |
| **Frase clave** | "Si esto ayuda a otro padre, vale la pena reportarlo." |

**Implicaciones de diseño:**
- Formulario de reporte máximo 3 campos obligatorios — María no tiene paciencia para formularios largos.
- Anonimato visible desde el primer momento: "Tu identidad no se guarda".
- Texto grande y botones obvios — María no busca opciones ocultas en menús.

---

## 2. MAPA DE EMOCIONES POR FLUJO

Cada pantalla debe gestionar una emoción específica. El diseño no es neutral: activamente tranquiliza o empodera.

### 2.1 Flujo de Búsqueda y Reporte

```
LANDING PAGE
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: CURIOSIDAD / PREOCUPACIÓN  │
│  Objetivo: Generar confianza        │
│  ─────────────────────────────────  │
│  • Logo visible + tagline clara      │
│  • "Buscar número" como CTA principal│
│  • Badge de anonimato visible       │
│  • Sin barreras de registro         │
└─────────────────────────────────────┘
     │
     ▼
BUSCADOR / RESULTADO
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: ANSIEDAD → ALIVIO/ACCIÓN   │
│  Objetivo: Claridad en 2 segundos    │
│  ─────────────────────────────────  │
│  • Input simple, teclado numérico   │
│  • Resultado cromático:             │
│    🟢 VERDE: "Sin reportes"         │
│    🟡 AMARILLO: "1-2 reportes"      │
│    🔴 ROJO: "Múltiples reportes"    │
│  • CTA claro según resultado        │
│  • Botón "¿Qué significa esto?"     │
└─────────────────────────────────────┘
     │
     ▼ (si rojo/amarillo)
FORMULARIO DE REPORTE
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: DETERMINACIÓN             │
│  Objetivo: Empoderamiento            │
│  ─────────────────────────────────  │
│  • Wizard de 3 pasos                │
│  • Barra de progreso: 3 puntos      │
│  • Campos mínimos obligatorios      │
│  • Badge "Anonimato garantizado"     │
│  • Botón "Atrás" siempre visible    │
└─────────────────────────────────────┘
     │
     ▼
CONFIRMACIÓN
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: ALIVIO → ORGULLO           │
│  Objetivo: Validación moral          │
│  ─────────────────────────────────  │
│  • Animación: escudo cerrándose      │
│  • Mensaje: "Hiciste lo correcto"    │
│  • Guía de acción siguiente          │
│  • Recursos de apoyo                 │
│  • Botón "Reportar otro" (opcional) │
└─────────────────────────────────────┘
```

### 2.2 Flujo de Panel Administrativo (Autoridades)

```
LOGIN ADMIN
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: SERIEDAD                  │
│  Objetivo: Profesionalismo          │
│  ─────────────────────────────────  │
│  • Sin animaciones decorativas      │
│  • Layout denso, datos primero      │
│  • Filtros avanzados visibles       │
│  • Acciones en tabla, no en modales │
└─────────────────────────────────────┘
     │
     ▼
DASHBOARD
     │
     ▼
┌─────────────────────────────────────┐
│  Estado: EFICIENCIA                 │
│  Objetivo: Toma de decisiones        │
│  ─────────────────────────────────  │
│  • KPIs arriba: reportes 24h,      │
│    pendientes, verificados           │
│  • Tabla con estado y prioridad      │
│  • Acciones bulk: verificar,         │
│    archivar, exportar                │
│  • Sin distracciones visuales        │
└─────────────────────────────────────┘
```

---

## 3. HEURÍSTICAS DE USABILIDAD PARA ESTE CONTEXTO

Reglas no negociables. Cada violación debe ser justificada ante el equipo.

| Heurística | Regla | Cómo se mide |
|------------|-------|-------------|
| **H1: Rapidez para reportar** | Máximo 3 toques desde landing hasta reporte enviado | Test de usuario: cronometrado |
| **H2: Sin registro obligatorio** | Nunca pedir cuenta antes de reportar | Auditoría de flujo de cada pantalla |
| **H3: Formulario minimalista** | Máximo 3 campos obligatorios en reporte | Revisión de schema de formulario |
| **H4: Comprensión inmediata** | Resultado de búsqueda comprensible en 2 segundos | Test de 5 segundos con usuarios |
| **H5: Ayuda siempre visible** | Botón de ayuda/FAQ accesible desde cualquier pantalla | Revisión de layout en todas las vistas |
| **H6: Sin revictimización** | El formulario no pregunta datos personales del usuario ni del menor | Revisión de copy de cada campo |
| **H7: Acción unidireccional** | Una vez en reporte, el usuario sabe siempre dónde está y cómo salir | Test de navegación con personas estresadas |
| **H8: Retroalimentación inmediata** | Cada acción tiene respuesta visual en <300ms | Medición con Lighthouse/Performance API |
| **H9: Friction intencional** | Confirmación clara antes de enviar reporte (evita errores) | Revisión de modal de confirmación |
| **H10: Salida segura** | Botón "Atrás" o "Cancelar" visible en todo momento | Revisión de componentes de navegación |

### 3.1 Wireframe ASCII: Landing Page (Mobile)

```
┌─────────────────────────────┐
│                             │
│      [LOGO ESCUDO]          │
│    Semáforo de Confianza    │
│                             │
│  Verifica contactos         │
│  sospechosos en segundos    │
│                             │
│  ┌─────────────────────┐    │
│  │  📞 Buscar número  │    │
│  └─────────────────────┘    │
│                             │
│  [ ? ] ¿Cómo funciona?      │
│                             │
│  ┌─────────────────────┐    │
│  │  📝 Reportar ahora   │    │
│  └─────────────────────┘    │
│                             │
│  🔒 Anonimato garantizado   │
│                             │
├─────────────────────────────┤
│  [Buscar] [Reportar] [Rec.] │
└─────────────────────────────┘
```

### 3.2 Wireframe ASCII: Resultado de Búsqueda (Rojo)

```
┌─────────────────────────────┐
│                             │
│  [🔴] ALERTA                 │
│                             │
│  Este número tiene            │
│  12 reportes previos          │
│                             │
│  ┌─────────────────────┐    │
│  │  ⚠️ Reportar ahora  │    │
│  └─────────────────────┘    │
│                             │
│  Último reporte: hace 3 días│
│  Categoría: Contacto        │
│  inapropiado con menor      │
│                             │
│  [¿Qué debo hacer?]         │
│                             │
├─────────────────────────────┤
│  [Buscar] [Reportar] [Rec.] │
└─────────────────────────────┘
```

---

## 4. DISEÑO MOBILE-FIRST (80% de usuarios)

### 4.1 Navegación Bottom Bar

```
┌─────────────────────────────┐
│                             │
│         CONTENIDO           │
│                             │
│                             │
│                             │
│                             │
├─────────────────────────────┤
│  🔍 Buscar  📝 Reportar  📚 Recursos  │
└─────────────────────────────┘
```

| Tab | Icono | Acción principal |
|-----|-------|-------------------|
| **Buscar** | 🔍 | Input de número + resultado |
| **Reportar** | 📝 | Wizard de 3 pasos |
| **Recursos** | 📚 | Guías, líneas de ayuda, FAQs |

**Reglas de la bottom bar:**
- Altura mínima: 56px (recomendado: 64px)
- Icono + etiqueta en 2 líneas
- Estado activo: color primario + icono filled
- Estado inactivo: color gris + icono outlined
- Nunca ocultar bottom bar en flujo de reporte (el usuario necesita salida visible)

### 4.2 Formulario: Wizard Mobile vs Desktop

**Mobile (3 pasos):**
```
Paso 1/3                Paso 2/3                Paso 3/3
┌─────────┐           ┌─────────┐           ┌─────────┐
│  ● ○ ○  │           │  ● ● ○  │           │  ● ● ●  │
│         │           │         │           │         │
│ Tipo de │           │ Datos   │           │ Evidencia│
│ contacto│           │ y desc  │           │ y envío  │
│ [chip]  │           │ [input] │           │ [drag]  │
│ [chip]  │           │ [area]  │           │ [check] │
│ [chip]  │           │         │           │         │
│         │           │         │           │         │
│ [Sig.]  │           │[Atrás]  │           │[Atrás]  │
│         │           │[Sig.]   │           │[Enviar] │
└─────────┘           └─────────┘           └─────────┘
```

**Desktop (todo en una pantalla):**
```
┌─────────────────────────────────────────────┐
│  Tipo de contacto    │  Datos              │
│  [chip] [chip]       │  [input]            │
│  [chip] [chip]       │  [textarea]         │
│                      │                     │
│  Evidencia           │  Confirmación        │
│  [drag-drop zone]    │  [✓] Anonimato      │
│                      │  [Enviar reporte]    │
└─────────────────────────────────────────────┘
```

### 4.3 Input de Búsqueda

```
┌─────────────────────────────────────┐
│  📞  +57 300 123 4567      [Buscar] │
└─────────────────────────────────────┘
```

| Atributo | Valor | Justificación |
|----------|-------|---------------|
| `type="tel"` | Teclado numérico | El 95% de búsquedas son números de celular |
| `inputmode="numeric"` | Números primero | Reduce errores de tipeo |
| `placeholder="+57 300 123 4567"` | Ejemplo con formato | Usuario sabe qué formato esperar |
| Full-width | 100% del ancho menos padding | El input es la acción principal |
| Altura | 48px mínimo | Tactilidad en dedos gruesos o temblor |

### 4.4 Botones: Tamaños y Estados

```
┌─────────────────────────────────────┐
│  Estado normal                      │
│  ┌─────────────────────┐            │
│  │  Reportar ahora     │  48px alto │
│  └─────────────────────┘            │
│                                     │
│  Estado hover/active                │
│  ┌─────────────────────┐            │
│  │  Reportar ahora     │  fondo más │
│  └─────────────────────┘  oscuro 5% │
│                                     │
│  Estado disabled                    │
│  ┌─────────────────────┐            │
│  │  Reportar ahora     │  50% opac  │
│  └─────────────────────┘            │
│                                     │
│  Estado loading                     │
│  ┌─────────────────────┐            │
│  │  ○ Enviando...      │  spinner  │
│  └─────────────────────┘            │
└─────────────────────────────────────┘
```

| Tipo | Altura | Padding horizontal | Radio | Uso |
|------|--------|-------------------|-------|-----|
| **Primario** | 48px | 24px | 8px | CTA principal (reportar, buscar) |
| **Secundario** | 44px | 20px | 8px | Acción alternativa (atrás, cancelar) |
| **Terciario** | 40px | 16px | 6px | Links, opciones menores |
| **Chip** | 36px | 12px | 18px | Selección de tipo de contacto |

---

## 5. ACCESIBILIDAD PARA CONTEXTO DE ESTRÉS

El usuario puede estar en estado de alerta: visión afectada, temblor, dificultad para concentrarse, posiblemente llorando. El diseño debe funcionar en estas condiciones.

### 5.1 Especificaciones de Accesibilidad

| Aspecto | Especificación | Cómo se implementa |
|---------|---------------|---------------------|
| **Contraste** | WCAG AA como mínimo, AAA preferido | Ratio 4.5:1 para texto normal, 7:1 para textos importantes |
| **Tamaño de texto** | 16px mínimo, 18px preferido, 20px para alertas | Nunca usar `font-size: 14px` para contenido legible |
| **Botones** | Mínimo 44px de alto, área táctil 48x48dp | Nunca esconder botones en menús hamburguesa |
| **Modales** | Prohibidos excepto para confirmación crítica | Usar inline expansion en lugar de popups |
| **Screen reader** | Todo el contenido navegable por voz | ARIA labels en resultados, botones, formularios |
| **Reducción de movimiento** | Respetar `prefers-reduced-motion` | Animaciones suaves por defecto, desactivables |
| **Zoom** | Funcional hasta 200% sin pérdida de layout | Layout fluido, no breakpoints rígidos |
| **Errores** | Mensajes de error en rojo + icono + texto claro | Nunca solo color para indicar error |

### 5.2 Colores: Accesibles y Emocionalmente Correctos

```
┌─────────────────────────────────────────────────────┐
│  PALETA DE SEMÁFORO                                 │
│                                                     │
│  🟢 VERDE: #2E7D32 (éxito, alivio)                 │
│     Contrast ratio sobre blanco: 5.8:1 ✓            │
│                                                     │
│  🟡 AMARILLO: #F9A825 (precaución)                  │
│     Contrast ratio sobre blanco: 3.2:1 → fondo #FFF8E1│
│     Contrast ratio sobre fondo crema: 5.1:1 ✓       │
│                                                     │
│  🔴 ROJO: #C62828 (alerta)                          │
│     Contrast ratio sobre blanco: 7.2:1 ✓            │
│                                                     │
│  🔵 PRIMARIO: #1565C0 (confianza, acción)           │
│     Contrast ratio sobre blanco: 6.9:1 ✓            │
│                                                     │
│  ⚫ TEXTO: #212121 (principal)                       │
│  ⚪ FONDO: #FFFFFF (principal)                      │
│  🔘 SECUNDARIO: #757575 (texto secundario)           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 5.3 Contexto de Estrés: Checklist de Diseño

- [ ] El usuario puede completar una búsqueda con una mano (thumb zone)
- [ ] El usuario puede leer todo el contenido sin hacer zoom
- [ ] El usuario puede encontrar el botón de ayuda sin buscarlo
- [ ] El usuario puede cancelar en cualquier momento sin consecuencias
- [ ] El usuario no necesita recordar información entre pasos
- [ ] El usuario recibe confirmación visual de cada acción
- [ ] El usuario no ve publicidad en momentos de estrés
- [ ] El usuario puede usar la app en un ambiente ruidoso (sin depender de audio)

---

## 6. MICRO-INTERACCIONES QUE TRANQUILIZAN

Las animaciones no son decorativas: son señales emocionales. Deben ser suaves, rápidas y significativas.

### 6.1 Catálogo de Micro-interacciones

| Acción | Animación | Duración | Significado emocional |
|--------|-----------|----------|----------------------|
| **Enviar reporte** | Escudo se cierra, brillo suave | 300ms | "Protección activada" |
| **Búsqueda en progreso** | Spinner suave, ondas circulares | continuo | "Estamos buscando, no te preocupes" |
| **Resultado verde** | Checkmark + fade in suave | 200ms | "Estás a salvo, alivio" |
| **Resultado amarillo** | Icono de precaución + pulso suave | 250ms | "Atención, pero no pánico" |
| **Resultado rojo** | Transición suave, no alerta abrupta | 300ms | "Hay algo que saber, pero estás informado" |
| **Copiar hash** | Toast pequeño "Copiado ✓" | 2000ms visible | "Confirmación sin interrupción" |
| **Paso completado** | Punto de progreso se rellena | 150ms | "Avanzas, vas bien" |
| **Error de validación** | Shake suave + rojo | 300ms | "Algo falta, corrígelo fácilmente" |
| **Botón hover** | Escala 1.02 + sombra suave | 150ms | "Esto es clickeable" |
| **Pull-to-refresh** | Escudo rota suavemente | 1000ms | "Actualizando protección" |

### 6.2 Principios de Animación

```
DURACIÓN RECOMENDADA
─────────────────────
Micro-interacciones: 150-300ms
Transiciones de pantalla: 200-300ms
Feedback de error: 200-300ms (shake)
Mensajes de confirmación: 2000-3000ms visible
─────────────────────
NUNCA MÁS DE 500ms: El usuario quiere velocidad en momentos de estrés.
```

| Principio | Descripción |
|-----------|-------------|
| **Easing** | `cubic-bezier(0.4, 0, 0.2, 1)` — suave, natural |
| **Dirección** | Las transiciones entran desde abajo (progreso), salen hacia arriba (retroceso) |
| **Reducción** | Respetar `prefers-reduced-motion: reduce` — desactivar animaciones excepto feedback esencial |
| **Consistencia** | Mismo easing en toda la app para crear predictibilidad |
| **Propósito** | Cada animación debe comunicar un estado, no decorar |

### 6.3 Animación del Escudo (Especial)

```
FASE 1: Búsqueda          FASE 2: Procesando        FASE 3: Confirmado
┌─────────┐               ┌─────────┐              ┌─────────┐
│  ╭───╮  │               │  ╭───╮  │              │  ╭───╮  │
│  │   │  │   ────►       │  │ ✓ │  │   ────►    │  │ ⚡ │  │
│  ╰───╯  │               │  ╰───╯  │              │  ╰───╯  │
│  abierto │               │  medio  │              │ cerrado │
└─────────┘               └─────────┘              └─────────┘
  0ms                        150ms                     300ms

Colores:
• Fase 1: Gris claro (#E0E0E0)
• Fase 2: Azul primario (#1565C0)
• Fase 3: Verde éxito (#2E7D32) + brillo sutil
```

---

## 7. PRINCIPIOS DE CONFIANZA VISUAL

La app debe *parecer* confiable antes de que el usuario la use. La confianza se construye en milisegundos.

### 7.1 Elementos de Confianza Visual

| Elemento | Ubicación | Implementación |
|----------|-----------|---------------|
| **Logo** | Header, favicon, splash screen | Escudo + semáforo estilizado. Vector, no raster. |
| **Badge "Anonimato garantizado"** | Arriba del formulario de reporte | Icono de candado + texto. Visible desde el primer paso. |
| **Badge "Sin cookies, sin tracking"** | Footer de todas las páginas | Texto + icono de privacidad. Sin enlaces a políticas largas. |
| **HTTPS lock** | Browser chrome (automático) | Certificado válido, HSTS habilitado. |
| **Sin publicidad** | Todo el flujo crítico | Nunca banners, popups, ni monetización en búsqueda/reporte. |
| **Sin distracciones** | Flujo de reporte | No notificaciones push, no modales de marketing. |
| **Transparencia** | Footer/página de información | Explicar qué se hace con los datos, en 3 viñetas o menos. |

### 7.2 Layout de Confianza: Landing Page

```
┌─────────────────────────────────────────────┐
│                                             │
│  [LOGO]  Semáforo de Confianza              │
│                                             │
│  Verifica contactos sospechosos             │
│  en segundos. Sin registro.                 │
│  Sin tracking.                              │
│                                             │
│  ┌─────────────────────────┐                │
│  │  📞  +57 300 123 4567  │                │
│  └─────────────────────────┘                │
│                                             │
│  [🔒 Buscar ahora]                          │
│                                             │
│  ─────────────────────────────────────     │
│                                             │
│  🛡️ Anonimato garantizado                   │
│  🚫 Sin cookies, sin tracking               │
│  🔒 Conexión cifrada                        │
│                                             │
├─────────────────────────────────────────────┤
│  [Buscar]  [Reportar]  [Recursos]           │
└─────────────────────────────────────────────┘
```

### 7.3 Mensajes de Confianza

| Contexto | Mensaje | Por qué funciona |
|----------|---------|-----------------|
| **Antes de reportar** | "Tu identidad no se guarda. Ni siquiera nosotros sabemos quién eres." | Elimina miedo a represalias |
| **Durante reporte** | "Esta información ayuda a proteger a otros padres." | Da propósito al esfuerzo |
| **Después de reporte** | "Gracias. Hiciste lo correcto. Tu reporte será revisado." | Valida la acción moral |
| **En footer** | "No usamos cookies. No guardamos tu IP. No hay publicidad." | Transparencia radical |

---

## 8. FORMULARIO DE REPORTE: UX POR PASOS

El formulario es el momento de mayor fricción emocional. Debe ser rápido, respetuoso y empoderador.

### 8.1 Wizard de 3 Pasos

```
┌─────────────────────────────────────────────────────┐
│  Barra de progreso:  ●  ○  ○                       │
│                                                     │
│  PASO 1: ¿Qué tipo de contacto es?                 │
│                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  📱     │  │  💬     │  │  📸     │           │
│  │ Celular │  │ Red     │  │ Contenido│           │
│  │         │  │ social  │  │ inapropiado│         │
│  └─────────┘  └─────────┘  └─────────┘           │
│                                                     │
│  ┌─────────┐  ┌─────────┐                         │
│  │  📧     │  │  🌐     │                           │
│  │ Email   │  │ Sitio   │                           │
│  │         │  │ web     │                           │
│  └─────────┘  └─────────┘                           │
│                                                     │
│  [Selecciona uno para continuar]                    │
│                                                     │
│  Seleccionado: 📱 Celular                           │
│                                                     │
│  [        Atrás        ] [        Siguiente        ]│
└─────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────┐
│  Barra de progreso:  ●  ●  ○                       │
│                                                     │
│  PASO 2: Identificador y descripción                 │
│                                                     │
│  Número o identificador                             │
│  ┌─────────────────────────────────────┐           │
│  │  +57 300 123 4567                  │           │
│  └─────────────────────────────────────┘           │
│                                                     │
│  ¿Qué te pareció sospechoso?                        │
│  ┌─────────────────────────────────────┐           │
│  │ "Me contactó diciendo que gané un   │           │
│  │  premio y pidió fotos de mi hija"   │           │
│  │                                     │           │
│  │                                     │           │
│  └─────────────────────────────────────┘           │
│                                                     │
│  [        Atrás        ] [        Siguiente        ]│
└─────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────┐
│  Barra de progreso:  ●  ●  ●                       │
│                                                     │
│  PASO 3: Evidencia y confirmación                    │
│                                                     │
│  📎 Adjunta evidencia (opcional)                    │
│  ┌─────────────────────────────────────┐           │
│  │                                     │           │
│  │    [Arrastra o toca para subir]     │           │
│  │                                     │           │
│  │    Capturas de pantalla, fotos,     │           │
│  │    videos relacionados              │           │
│  │                                     │           │
│  └─────────────────────────────────────┘           │
│                                                     │
│  [✓] Confirmo que esta información es veraz        │
│      y la comparto de forma anónima.                │
│                                                     │
│  [🛡️ Enviar reporte anónimo]                      │
│                                                     │
│  [        Atrás        ]                            │
└─────────────────────────────────────────────────────┘
```

### 8.2 Especificaciones de Campos

| Campo | Paso | Obligatorio | Tipo | Placeholder | Validación |
|-------|------|-------------|------|-------------|------------|
| Tipo de contacto | 1 | Sí | Chip seleccionable | — | Exactamente 1 selección |
| Identificador | 2 | Sí | Texto | "+57 300 123 4567" | Min 5 caracteres |
| Descripción | 2 | Sí | Textarea | "¿Qué te pareció sospechoso?" | Min 20 caracteres |
| Evidencia | 3 | No | File upload | "Arrastra o toca para subir" | Max 10MB, img/video/pdf |
| Confirmación | 3 | Sí | Checkbox | — | Debe estar marcada |

### 8.3 Barra de Progreso

```
MÓVIL (3 puntos)                    DESKTOP (3 puntos con etiquetas)
┌─────────┐                        ┌─────────────────────────────────┐
│ ●  ○  ○ │                        │  ●────●────○                    │
│         │                        │  Tipo  Datos  Enviar           │
│  Paso 1 │                        │  Paso  Paso   Paso             │
│  de 3   │                        │  1     2      3                │
└─────────┘                        └─────────────────────────────────┘
```

**Reglas de la barra de progreso:**
- Usar puntos, no porcentaje (reduce ansiedad de "¿cuánto falta?")
- Punto completado: relleno con color primario
- Punto actual: borde grueso + color primario
- Punto futuro: borde fino + gris
- Transición entre pasos: 150ms de fade

### 8.4 Navegación: Botón "Atrás"

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [  ← Atrás  ]              [  Siguiente →  ]       │
│                                                     │
│  Posición: izquierda        Posición: derecha        │
│  Estilo: secundario         Estilo: primario         │
│  Acción: guarda progreso    Acción: valida y avanza  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Reglas del botón Atrás:**
- Siempre visible, nunca deshabilitado
- Guarda progreso del paso actual (no pierde datos)
- En paso 1, "Atrás" lleva a la landing page
- Nunca usar botón de navegador del sistema como única salida

---

## 9. CHECKLIST UX PARA DESARROLLADORES

Esta checklist debe ser verificada antes de cada release. Cada ítem debe pasar un test manual.

### 9.1 Checklist Funcional

- [ ] **Usuario puede reportar en menos de 2 minutos**
  - Test: Cronometrar desde landing hasta confirmación de envío
  - Target: < 2 minutos para usuario first-time

- [ ] **Sin registro obligatorio**
  - Test: Intentar reportar sin crear cuenta
  - Target: Flujo completo sin pedir email, teléfono, ni nombre

- [ ] **Resultado de búsqueda comprensible en 2 segundos**
  - Test: Mostrar resultado a 5 personas sin contexto
  - Target: 4/5 personas entienden el significado sin explicación

- [ ] **Botón de ayuda visible en todas las pantallas**
  - Test: Navegar por toda la app buscando el botón de ayuda
  - Target: Siempre accesible en ≤ 2 toques desde cualquier pantalla

- [ ] **Formulario no revictimiza con preguntas invasivas**
  - Test: Revisar cada campo del formulario
  - Target: Ningún campo pide nombre del usuario, del menor, dirección, ni datos personales identificables

- [ ] **Animaciones tranquilizan, no distraen**
  - Test: Revisar cada animación con el equipo
  - Target: Ninguna animación dura > 500ms, ninguna es puramente decorativa

- [ ] **Accesible en móvil con una mano**
  - Test: Usar app con una mano derecha, luego izquierda
  - Target: Todos los botones principales alcanzables sin estirar el dedo

- [ ] **Contraste WCAG AA en todo**
  - Test: Usar herramienta de contraste (ej: Stark plugin)
  - Target: Ratio ≥ 4.5:1 para todo texto, ≥ 3:1 para componentes UI

- [ ] **Mensaje post-reporte incluye guía de acción y recursos**
  - Test: Enviar reporte de prueba
  - Target: Pantalla de confirmación incluye al menos 3 recursos de ayuda (líneas de emergencia, guías, etc.)

### 9.2 Checklist Técnico

- [ ] Lighthouse Accessibility score ≥ 90
- [ ] TTI (Time to Interactive) < 3 segundos en 4G
- [ ] FCP (First Contentful Paint) < 1.5 segundos
- [ ] Tamaño de bundle < 200KB (excluyendo imágenes)
- [ ] Funciona offline (service worker cachea assets críticos)
- [ ] PWA installable (manifest válido, íconos correctos)
- [ ] Todos los formularios funcionan con autofill desactivado
- [ ] No hay modales que bloqueen sin botón de cerrar visible
- [ ] Keyboard navigation funciona en todo el flujo (tab, enter, escape)
- [ ] Screen reader anuncia correctamente resultados de búsqueda

### 9.3 Checklist Emocional

- [ ] El usuario se siente más tranquilo después de usar la app que antes
- [ ] El usuario siente que "hizo algo" después de reportar
- [ ] El usuario no siente que está "exagerando" al reportar
- [ ] El usuario entiende qué pasa con su reporte después de enviarlo
- [ ] El usuario siente que la app está de su lado, no del agresor
- [ ] El usuario puede usar la app sin que alguien más se entere (discreción)
- [ ] El usuario no siente que la app está "vendiendo" algo
- [ ] El usuario siente que la app es profesional y confiable

---

## APÉNDICE A: VOCABULARIO CONTROLADO

Palabras permitidas y prohibidas en la interfaz. El tono debe ser serio, empático y accionable.

| ✅ Usar | ❌ Evitar | 📝 Razón |
|---------|----------|----------|
| "Contacto sospechoso" | "Predador" | Neutral, no alarmista |
| "Reportar de forma anónima" | "Denunciar" | "Denunciar" suena a proceso legal largo |
| "Verificar" | "Investigar" | "Investigar" suena a algo que el usuario no puede hacer |
| "Hiciste lo correcto" | "Gracias por tu denuncia" | Enfocado en la acción moral, no en el sistema |
| "Protección activada" | "Reporte enviado" | Emocionalmente más significativo |
| "Anonimato garantizado" | "Privacidad protegida" | "Garantizado" es más fuerte que "protegida" |
| "Sin reportes previos" | "Limpio" | "Limpio" es ambiguo |
| "Reportes previos encontrados" | "Peligro" | Factual, no alarmista |
| "¿Qué debo hacer?" | "Ayuda" | Acción directa, no categoría |
| "Recursos de apoyo" | "Enlaces útiles" | "Recursos de apoyo" suena a ayuda real |

---

## APÉNDICE B: REFERENCIAS DE DISEÑO

Esta guía se inspiró en los siguientes principios y referentes:

1. **Google Material Design 3** — Componentes base, tokens de color, motion guidelines
2. **WCAG 2.1 AA/AAA** — Estándares de accesibilidad
3. **Calm Technology** — Principio de tecnología que no demanda atención innecesaria
4. **Trauma-Informed Design** — Diseño que no revictimiza ni agrega estrés al usuario
5. **Nielsen's 10 Usability Heuristics** — Adaptadas para contexto de estrés emocional
6. **Apple Human Interface Guidelines** — Accesibilidad, tactilidad, claridad

---

> **Nota para el equipo de desarrollo:**  
> Esta guía no es un documento estático. Si encuentras un caso de uso no cubierto, un usuario que no encaja en las personas, o una interacción que genera confusión, documenta el problema y propón una actualización. El diseño evoluciona con los usuarios reales.

---

**Documento generado para:** ODIN-CEO  
**Plataforma:** Semáforo de Confianza  
**Fecha de generación:** 2026-06-13  
**Versión:** 1.0  
**Próxima revisión:** Cuando se completen los primeros 10 tests de usuario
