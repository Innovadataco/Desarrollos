# DISEÑO UI/UX — Semáforo de Confianza

**Fecha:** 13 de junio de 2026  
**Versión:** 1.0  
**Autor:** ZEUS (diseño dirigido por CEO Jelkin Zair Carrillo Franco)  
**Estado:** Directiva de diseño activa

---

## 🎨 VISIÓN DE DISEÑO

> **"Una aplicación que transmita seguridad, tranquilidad y empoderamiento desde el primer pixel. Cada interacción debe decir: 'estás protegido, estás haciendo lo correcto, y no estás solo'."**

El diseño no es decorativo — es funcional emocional. Un padre que entra a reportar un contacto sospechoso de su hijo está en estado de alerta, posiblemente ansioso. El diseño debe:
- **Reducir la ansiedad** (no agregarla)
- **Generar confianza** (no parecer amateur o sospechoso)
- **Empoderar** (el usuario siente que tiene control)
- **Motivar la acción** (reportar no es un trámite, es un acto de protección)

---

## 🌈 PALETA DE COLORES — "Seguridad Auténtica"

### Colores Primarios (Identidad de marca)

| Nombre | HEX | Uso | Emoción |
|--------|-----|-----|---------|
| **Azul Profundo** | `#1A3A5C` | Headers, navbar, fondos principales | Confianza, seriedad, profesionalismo |
| **Azul Tranquilidad** | `#4A90D9` | Botones primarios, acentos, links | Calma, accesibilidad, "todo está bien" |
| **Blanco Nube** | `#F8FAFC` | Fondos de secciones, cards | Limpieza, pureza, espacio para respirar |

### Colores del Semáforo (Sistema de alerta)

| Nombre | HEX | Significado | Uso |
|--------|-----|-------------|-----|
| **Verde Esperanza** | `#27AE60` | Sin reportes | "Este contacto está limpio. Tranquilidad." |
| **Amarillo Cuidado** | `#F39C12` | Reportes dudosos/spam | "Atención. Hay algo que revisar." |
| **Rojo Protección** | `#E74C3C` | Múltiples reportes de comportamiento depredador | **NO** "peligro" sino **"protección activada"** |

> **Nota clave sobre el Rojo:** El rojo no es "alerta de peligro genérico". Es "protección activada". El mensaje debe ser: "La comunidad está protegiendo a tu hijo. Actúa." No "¡Peligro! ¡Pánico!".

### Colores Secundarios (Detalles y estados)

| Nombre | HEX | Uso |
|--------|-----|-----|
| **Coral Calidez** | `#FF6B6B` | Badges de "reporte reciente", iconos de acción urgente |
| **Verde Menta** | `#48CFAD` | Éxito, confirmación, hash de reporte |
| **Lavanda Descanso** | `#9B59B6` | Secciones de contención, recursos de apoyo |
| **Gris Piedra** | `#7F8C8D` | Textos secundarios, metadatos, deshabilitado |
| **Negro Suave** | `#2C3E50` | Textos principales, títulos |

### Gradients (Efectos bonitos, modernos)

```css
/* Hero gradient — seguridad que se siente */
.hero-gradient {
  background: linear-gradient(135deg, #1A3A5C 0%, #4A90D9 50%, #27AE60 100%);
}

/* Card glow — confianza tangible */
.card-trust {
  box-shadow: 0 4px 20px rgba(74, 144, 217, 0.15);
  transition: all 0.3s ease;
}
.card-trust:hover {
  box-shadow: 0 8px 30px rgba(74, 144, 217, 0.25);
  transform: translateY(-2px);
}

/* Semáforo glow — protección que brilla */
.semaforo-rojo {
  box-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
  animation: pulse-protection 2s infinite;
}
@keyframes pulse-protection {
  0%, 100% { box-shadow: 0 0 20px rgba(231, 76, 60, 0.3); }
  50% { box-shadow: 0 0 30px rgba(231, 76, 60, 0.5); }
}
```

---

## 🔤 TIPOGRAFÍA — "Lenguaje Seguro y Tranquilo"

### Familia Principal: Inter o Roboto

| Uso | Fuente | Peso | Tamaño | Característica |
|-----|--------|------|--------|----------------|
| **Títulos H1** | Inter | 700 (Bold) | 32-40px | Seguro, firme, sin ser agresivo |
| **Títulos H2** | Inter | 600 (SemiBold) | 24-28px | Claro, estructurado |
| **Títulos H3** | Inter | 600 (SemiBold) | 18-20px | Organizado, jerárquico |
| **Cuerpo** | Inter | 400 (Regular) | 16px | Legible, calmado, espaciado generoso (1.6 line-height) |
| **Botones** | Inter | 600 (SemiBold) | 16px | Acción clara, sin miedo |
| **Etiquetas** | Inter | 500 (Medium) | 12-14px | Uppercase, letter-spacing 0.5px |
| **Números/Hash** | JetBrains Mono | 400 | 14px | Hash de reporte, scores, técnicos |

> **Por qué Inter:** Diseñada para pantallas, legible en todos los tamaños, neutral sin ser fría. No es agresiva ni infantil. Es adulta, madura, confiable.

> **Por qué JetBrains Mono:** Para códigos de reporte, scores, y datos técnicos. Transmite precisión y seriedad.

---

## 🧱 COMPONENTES CLAVE — Diseño por Pantalla

### 1. LANDING PAGE (Primera impresión = confianza)

**Estructura:**
```
┌─────────────────────────────────────────────┐
│  [Logo: Escudo + Semáforo]  [¿Qué es esto?] │
├─────────────────────────────────────────────┤
│                                             │
│  "Protege a tu hijo antes de que pase"      │
│  Consulta números, reporta contactos         │
│  sospechosos, mantente informado.            │
│                                             │
│  [🔍 Buscar un número]  [📝 Reportar]        │
│                                             │
├─────────────────────────────────────────────┤
│  📊 Semáforo de Confianza Comunitaria        │
│  [Verde] [Amarillo] [Rojo]                   │
│  "14,230 números consultados esta semana"    │
│  "1,847 reportes que protegieron a niños"    │
│                                             │
├─────────────────────────────────────────────┤
│  🛡️ Cómo funciona (3 pasos)                  │
│  1. Busca  →  2. Reporta  →  3. Protege     │
│                                             │
├─────────────────────────────────────────────┤
│  💚 "Nunca pedimos tu nombre. Nunca pedimos   │
│  tu identidad. Tu reporte es anónimo."      │
│                                             │
└─────────────────────────────────────────────┘
```

**Diseño:**
- Hero: gradiente Azul Profundo → Azul Tranquilidad, texto blanco
- Stats cards: fondo Blanco Nube, bordes redondeados (16px radius), sombra suave
- Iconografía: Líneas finas, estilo outline, nunca sólido pesado. Tamaño 24px.
- Animación: Las cards flotan suavemente al hacer scroll (parallax ligero)

### 2. BUSCADOR (El corazón del producto)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  🔍 Busca un número, username o email        │
│  [___________________________________] [🔍] │
│  "Ej: +573001234567, @ProGamer99,            │
│  correo@ejemplo.com"                        │
│                                             │
├─────────────────────────────────────────────┤
│  RESULTADO:                                  │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  🟢 NIVEL DE CONFIANZA: ALTO        │    │
│  │                                     │    │
│  │  Este identificador no tiene        │    │
│  │  reportes de la comunidad.          │    │
│  │  Puedes continuar con precaución    │    │
│  │  normal.                            │    │
│  │                                     │    │
│  │  [0 reportes | Última consulta: hoy]│    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  🟡 NIVEL DE CONFIANZA: MEDIO      │    │
│  │                                     │    │
│  │  Este identificador tiene 3         │    │
│  │  reportes por interacciones         │    │
│  │  dudosas. Recomendación: conversa   │    │
│  │  con tu hijo sobre este contacto.   │    │
│  │                                     │    │
│  │  [3 reportes | 1 de spam, 2 de     │    │
│  │  contacto inapropiado]              │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  🔴 NIVEL DE CONFIANZA: BAJO       │    │
│  │                                     │    │
│  │  ⚠️ ATENCIÓN: 14 reportes de        │    │
│  │  padres en los últimos 30 días.    │    │
│  │  Comportamiento reportado: solicitud│    │
│  │  de información personal a menores.  │    │
│  │                                     │    │
│  │  🔒 Recomendación: BLOQUEAR y NO     │    │
│  │  interactuar. Si ya hubo contacto,   │    │
│  │  guarda evidencia y contacta a       │    │
│  │  línea 141 del ICBF.               │    │
│  │                                     │    │
│  │  [14 reportes | 5 ciudades |         │    │
│  │  Score: 0.92/1.0]                  │    │
│  │                                     │    │
│  │  [📞 Línea 141] [📋 ¿Qué hacer?]   │    │
│  └─────────────────────────────────────┘    │
│                                             │
└─────────────────────────────────────────────┘
```

**Diseño detallado:**
- Input de búsqueda: Borde 2px Azul Tranquilidad, focus con glow suave, placeholder Gris Piedra
- Resultados: Card con borde izquierdo 4px del color del semáforo (verde/amarillo/rojo)
- Animación: Al aparecer el resultado, card hace un fade-in + slide-up de 20px (300ms, ease-out)
- Iconos: Emoji nativo + iconos SVG outline. Nunca iconos de alerta genéricos.

### 3. FORMULARIO DE REPORTE (Empoderamiento, no trámite)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  📝 Reportar un contacto sospechoso          │
│                                             │
│  "Tu reporte puede proteger a otros niños.   │
│  No necesitas identificarte."               │
│                                             │
│  ¿Qué tipo de contacto es?                   │
│  [📱 WhatsApp] [🎮 Videojuego] [📷 Red Social]│
│  [📧 Email] [💬 Otra]                         │
│                                             │
│  Identificador del contacto:                  │
│  [+57 300 123 4567________________]        │
│  "Número, username, o email del sospechoso"  │
│                                             │
│  ¿Qué ocurrió? (describe brevemente):        │
│  [                                          │
│   Mi hijo recibió mensajes pidiendo          │
│   fotos a cambio de dinero...               │
│  ___________________________________]        │
│                                             │
│  📎 Adjuntar evidencia (opcional):           │
│  [📷 Foto] [🎥 Video] [🎙️ Audio] [📄 Doc]    │
│  "Las capturas de pantalla ayudan a          │
│  autoridades. Se almacenan encriptadas."     │
│                                             │
│  ✅ Entiendo que este reporte es anónimo     │
│  y se enviará a autoridades para revisión.  │
│                                             │
│  [🚀 ENVIAR REPORTE ANÓNIMO]                 │
│                                             │
│  💚 "Tu identidad nunca se revela. Nunca."   │
│                                             │
└─────────────────────────────────────────────┘
```

**Diseño detallado:**
- Paso a paso: No mostrar todo de golpe. Wizard de 3 pasos: 1) Tipo de contacto, 2) Identificador + descripción, 3) Evidencia + confirmación
- Botones de tipo de contacto: Chips redondeados, icono + texto, selección con fondo Azul Tranquilidad + texto blanco
- Textarea: Bordes redondeados, placeholder con ejemplo real (no "Escribe aquí" sino un ejemplo concreto)
- Adjuntar evidencia: Botones de drag-and-drop visual, con iconos grandes y claros
- Botón de envío: Fondo Coral Calidez o Azul Tranquilidad, texto blanco, border-radius 12px, padding generoso
- Checkbox de confirmación: Texto pequeño, Gris Piedra, pero visible
- Frase de seguridad debajo del botón: Verde Menta, icono de escudo, centrada

**Micro-interacciones:**
- Al seleccionar tipo de contacto: chip hace un scale(1.05) + cambio de color (150ms)
- Al escribir en textarea: borde cambia a Azul Tranquilidad, contador de caracteres aparece
- Al adjuntar archivo: nombre aparece con animación de slide-in, icono de check verde
- Al enviar: botón cambia a "Enviando..." con spinner, luego "✅ Reporte enviado" + hash aparece con animación de confetti sutil (no infantil, elegante)

### 4. PANTALLA DE CONFIRMACIÓN (Hash + contención)

```
┌─────────────────────────────────────────────┐
│                                             │
│           ✅ REPORTE ENVIADO                 │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  Tu código de seguimiento:          │    │
│  │                                     │    │
│  │  #7F3A-9B21-C4D8                   │    │
│  │  [📋 Copiar]                       │    │
│  │                                     │    │
│  │  Guarda este código. Si necesitas  │    │
│  │  seguimiento, solo tú puedes usarlo.│    │
│  └─────────────────────────────────────┘    │
│                                             │
│  🧠 ¿Qué hacer ahora?                        │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  1. NO confrontes al contacto       │    │
│  │  2. Guarda toda la evidencia        │    │
│  │  3. Bloquea al contacto en la app   │    │
│  │  4. Habla con tu hijo con calma     │    │
│  │  5. Si hay material sensible,        │    │
│  │     contacta Línea 141 del ICBF    │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  📞 Recursos de apoyo:                       │
│  [Línea 141] [Te Protejo] [Fiscalía]        │
│                                             │
│  💚 "Gracias por proteger a tu comunidad.    │
│  Tu reporte ya está en manos de quienes      │
│  pueden actuar."                             │
│                                             │
└─────────────────────────────────────────────┘
```

**Diseño:**
- Hash: Fuente JetBrains Mono, fondo Blanco Nube, borde Verde Menta, botón de copiar al lado
- Guía de acción: Lista numerada con iconos, fondo Blanco Nube, bordes redondeados
- Botones de recursos: Chips con iconos de teléfono, color Lavanda Descanso
- Mensaje final: Texto centrado, Verde Menta, icono de escudo

### 5. PANEL DE ADMIN (Solo autoridades — serio, profesional, sobrio)

**Diseño diferente al frontend civil:**
- Paleta: Azul Profundo + Gris Piedra + Blanco Nube. Sin colores brillantes.
- Tipografía: Inter 400/500, tamaños más pequeños, densidad de información alta
- Layout: Tabla con filas compactas, filtros laterales, gráficos de barras sobrios
- Sin animaciones llamativas. Todo es funcional y rápido.
- Estado visual: badges pequeños (Nuevo, En revisión, Escalado, Cerrado) con colores sutiles

---

## ✨ PRINCIPIOS DE DISEÑO

### 1. **Seguridad Visual Primero**
Cada elemento debe transmitir "esto es seguro":
- HTTPS lock icon visible en footer
- "Anonimato garantizado" badge en formulario
- Escudo como icono principal de marca
- Sin tracking, sin cookies banner (porque no hay cookies)

### 2. **Lenguaje Empático, No Alarmista**

| ❌ NO | ✅ SÍ |
|-------|-------|
| "¡PELIGRO! ¡ALERTA ROJA!" | "Atención: La comunidad ha reportado este contacto. Protege a tu hijo." |
| "Reportar pedófilo" | "Reportar contacto inapropiado con menor" |
| "Evidencia" | "Información que ayuda a autoridades" |
| "Tu denuncia" | "Tu reporte anónimo" |
| "Criminal" | "Persona reportada por comportamiento depredador" |

### 3. **Calma en la Urgencia**
Cuando el semáforo es rojo, el diseño NO debe generar pánico:
- Rojo con fondo suave (no rojo brillante sobre blanco puro)
- Mensaje estructurado: qué pasó, qué hacer, quién contactar
- Botones de acción claros, no múltiples opciones que confundan
- Siempre incluir recurso de apoyo (línea 141, Te Protejo)

### 4. **Accesibilidad Inclusiva**
- Contrastes WCAG AA mínimo (todos los textos sobre fondos pasan validación)
- Tamaño de texto base 16px (no reducir para "que quepa todo")
- Botones mínimo 44px de alto (tactilidad móvil)
- Soporte para screen readers (aria-labels en todo)
- Modo oscuro opcional (fondo `#0F172A`, texto `#E2E8F0`)

### 5. **Efectos Modernos, Nunca Infantiles**

**Sí:**
- Sombras suaves y difusas (no sombras duras negras)
- Transiciones suaves (150-300ms, ease-in-out)
- Gradientes sutiles (nunca arcoíris)
- Micro-interacciones que recompensan (confeti sutil al enviar reporte)
- Glassmorphism ligero en cards (backdrop-filter: blur, fondo semi-transparente)

**No:**
- Animaciones de rebote exageradas
- Colores neón o saturados
- Iconos 3D o skeuomorfismo
- Fondos con patrones distractores
- Tipografía decorativa o script

---

## 📱 RESPONSIVE — Móvil Primero

El 80% de los usuarios serán padres en sus celulares. El diseño es móvil-first:

- **Ancho máximo:** 480px en móvil, 768px en tablet, 1200px en desktop
- **Navegación:** Bottom bar en móvil (Buscar, Reportar, Recursos), top bar en desktop
- **Formulario:** Wizard de pasos en móvil (no scroll infinito), todo en una pantalla en desktop
- **Buscador:** Input full-width, resultados en cards apiladas
- **Teclado:** Campos numéricos para teléfono, email para correos, text para descripción

---

## 🎯 COMPONENTES ATÓMICOS (Design System)

### Botones

```css
/* Botón Primario — Acción */
.btn-primary {
  background: linear-gradient(135deg, #4A90D9, #1A3A5C);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px 28px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(74, 144, 217, 0.3);
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 144, 217, 0.4);
}
.btn-primary:active {
  transform: translateY(0);
}

/* Botón Secundario — Reportar */
.btn-report {
  background: #E74C3C;
  color: white;
  border-radius: 12px;
  padding: 14px 28px;
  font-weight: 600;
  transition: all 0.2s ease;
}
.btn-report:hover {
  background: #C0392B;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

/* Botón Ghost — Recursos */
.btn-ghost {
  background: transparent;
  color: #4A90D9;
  border: 2px solid #4A90D9;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.2s ease;
}
.btn-ghost:hover {
  background: #4A90D9;
  color: white;
}
```

### Cards

```css
.card {
  background: #F8FAFC;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(74, 144, 217, 0.1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}
.card:hover {
  box-shadow: 0 4px 20px rgba(74, 144, 217, 0.1);
  transform: translateY(-2px);
}

/* Card de semáforo */
.card-semaforo-verde { border-left: 4px solid #27AE60; }
.card-semaforo-amarillo { border-left: 4px solid #F39C12; }
.card-semaforo-rojo { border-left: 4px solid #E74C3C; }
```

### Inputs

```css
.input {
  background: white;
  border: 2px solid #E2E8F0;
  border-radius: 12px;
  padding: 14px 16px;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  color: #2C3E50;
  transition: all 0.2s ease;
  width: 100%;
}
.input:focus {
  border-color: #4A90D9;
  box-shadow: 0 0 0 4px rgba(74, 144, 217, 0.1);
  outline: none;
}
.input::placeholder {
  color: #94A3B8;
  font-size: 14px;
}
```

---

## 🎬 ANIMACIONES Y TRANSICIONES

| Interacción | Animación | Duración | Easing |
|-------------|-----------|----------|--------|
| Carga de página | Fade-in de contenido | 400ms | ease-out |
| Aparece resultado | Slide-up + fade-in | 300ms | ease-out |
| Hover en card | translateY(-2px) + shadow | 200ms | ease |
| Click en botón | scale(0.98) | 100ms | ease-in |
| Envío de reporte | Spinner + cambio a check | 500ms | ease-in-out |
| Hash aparece | Typewriter effect + glow | 800ms | steps |
| Scroll a sección | Smooth scroll | 600ms | ease-in-out |
| Cambio de semáforo | Color transition suave | 400ms | ease |

---

## 🏷️ ICONOGRAFÍA

**Set:** Lucide React (línea fina, moderno, consistente)

**Iconos clave y su significado:**

| Icono | Uso | Significado emocional |
|-------|-----|----------------------|
| Shield | Logo principal | Protección, seguridad |
| Search | Buscador | Descubrimiento, control |
| AlertTriangle | Semáforo amarillo | Atención, no pánico |
| AlertOctagon | Semáforo rojo | Protección activada |
| CheckCircle | Éxito, confirmación | Todo bien, acción completada |
| Heart | Recursos de apoyo | Cuidado, contención |
| Lock | Anonimato | Privacidad, confianza |
| Eye | Ver reporte | Transparencia (solo admin) |
| Upload | Adjuntar evidencia | Contribución, ayuda |
| Phone | Línea de ayuda | Conexión, no estás solo |
| MessageCircle | Reportar | Comunicación, voz |
| Users | Comunidad | No estás solo, otros padres también |

> **Regla:** Todos los iconos son outline (línea), nunca sólido. Tamaño 20-24px. Color hereda del texto padre.

---

## 🌙 MODO OSCURO (Opcional)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0F172A;
    --bg-card: #1E293B;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --border: #334155;
    --accent: #4A90D9;
  }
}
```

- Fondo: Azul muy oscuro (no negro puro)
- Cards: Gris azulado oscuro
- Texto: Blanco suave (no blanco puro)
- Acentos: Azul Tranquilidad mantiene intensidad
- Semáforo: Colores se mantienen, pero con fondos más suaves

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

**Frontend (React + Tailwind):**
- [ ] Configurar fuentes Inter y JetBrains Mono en index.html
- [ ] Crear variables CSS con la paleta completa
- [ ] Implementar componentes atómicos (Button, Card, Input, Badge)
- [ ] Crear layout responsive (mobile-first)
- [ ] Implementar animaciones con Framer Motion o CSS transitions
- [ ] Agregar iconos Lucide React
- [ ] Crear modo oscuro con toggle
- [ ] Validar contraste WCAG AA en todas las combinaciones
- [ ] Testear en iOS Safari, Android Chrome, Desktop Chrome/Firefox

**Assets necesarios:**
- [ ] Logo SVG (escudo + semáforo)
- [ ] Favicon en múltiples tamaños
- [ ] Ilustraciones para landing (padre + hijo + dispositivo, estilo flat)
- [ ] Screenshots para PWA manifest
- [ ] OG image para redes sociales (1200x630)

---

> **Documento de diseño generado por ZEUS — Innovadataco**
> 
> *Directiva del CEO: Moderno, elegante, confianza, tranquilidad, colores auténticos, efectos bonitos, tipografía segura.*
