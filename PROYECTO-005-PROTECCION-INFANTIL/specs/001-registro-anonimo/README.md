# Módulo 1: Registro Anónimo de Reportes

## Propósito
Permitir a cualquier persona registrar un reporte de protección infantil de forma **completamente anónima** y segura.

## Principios de diseño

1. **Anonimato absoluto**: no se almacenan IPs, cookies, user-agents, device metadata ni ningún dato que permita rastrear al reportante.
2. **Encriptación en reposo**: todos los campos sensibles se encriptan con AES-256-GCM.
3. **Probabilidad, no verdad absoluta**: el sistema registra información, no emite juicios.
4. **Mínima retención**: el rate limiter usa memoria; las IPs no persisten más allá de la ventana de 1 hora.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servicio |
| POST | `/api/reportes` | Crear reporte anónimo |

### POST /api/reportes

**Request body:**
```json
{
  "reported_identifier": "+573001234567",
  "description": "Recibí mensajes inapropiados",
  "evidence": {
    "type": "text",
    "content": "captura de pantalla descriptiva"
  }
}
```

**Response 201:**
```json
{
  "report_hash": "b7a4a8295f1a0055df9e62eb456bce715ae2c85ce5d515370c0057ee474ed983",
  "reported_at": "2026-06-12T07:49:02.033943"
}
```

## Encriptación

- Cada campo sensible se encripta con una **DEK (Data Encryption Key)** aleatoria de 256 bits.
- La DEK se encripta con la **KEK (Key Encryption Key)** derivada de `REPORT_ENCRYPTION_KEY`.
- Formato almacenado: `[len_encrypted_dek: 2 bytes][encrypted_dek][nonce||tag||ciphertext]`.

## Rate limiting

- 5 reportes por IP por hora.
- Implementado en memoria; no hay persistencia de IPs.

## Tests

```bash
cd src/backend
source .venv/bin/activate
pytest -v
```

```bash
cd src/frontend
npm test
```
