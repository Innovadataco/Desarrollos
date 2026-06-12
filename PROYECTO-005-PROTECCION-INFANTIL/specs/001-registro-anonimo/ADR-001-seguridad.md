# ADR-001: Seguridad y Anonimato

## Estado

Aceptado

## Contexto

El Proyecto 005 gestiona reportes de protección infantil. Los datos son altamente sensibles y los reportantes deben permanecer anónimos. Se requiere:

- Confidencialidad de la información en reposo.
- Anonimato del reportante (sin IP, user-agent, cookies ni metadata).
- Integridad de los datos (detección de manipulación).
- Disponibilidad básica protegida contra abuso (rate limiting).

## Decisión

Usar **AES-256-GCM** con una **DEK aleatoria por campo** y una **KEK derivada de una variable de entorno** de 32 bytes.

- Cada campo sensible (`reported_identifier`, `description`, `evidence_content`) se encripta con una DEK única.
- La DEK se encripta con la KEK y se almacena junto al valor encriptado.
- El modelo `Report` no incluye columnas de metadata identificable.
- Se implementa rate limiting por IP (5 reportes/hora) con fallback a memoria y soporte para Redis.

## Consecuencias

- **Positivas:**
  - Cumplimiento con requisitos de anonimato.
  - Encriptación autenticada que detecta tampering.
  - Escalabilidad del rate limiting mediante Redis.

- **Negativas:**
  - No se puede buscar por contenido encriptado, solo por `report_hash`.
  - La rotación de la KEK requiere re-encriptar todos los registros.
  - El rate limiting en memoria no escala entre workers.

## Alternativas rechazadas

- **RSA:** Más lento y complejo para datos de tamaño variable.
- **ChaCha20:** No está de forma nativa en el módulo `cryptography` de Python para este caso de uso.
- **Hash determinista del reportante:** Permitiría vincular reportes; se prefirió SHA-256 con nonce aleatorio.
