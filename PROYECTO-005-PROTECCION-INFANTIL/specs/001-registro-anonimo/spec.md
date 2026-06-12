# SPEC-001: Registro Anónimo de Números Telefónicos

## Contexto
Los padres deben poder reportar números telefónicos o usuarios que contactan a niños con fines de abuso, sin exponer su identidad.

## Requisitos Funcionales
1. El usuario accede a un formulario web sin necesidad de login
2. El formulario solicita: número telefónico o usuario a reportar, descripción del incidente, evidencia opcional (texto o imagen)
3. El sistema NO debe guardar IP, user-agent, cookies, ni metadata del dispositivo
4. El sistema debe encriptar todos los datos en reposo (AES-256)
5. El sistema debe generar un hash único del reporte para seguimiento interno (no vinculable al reportante)
6. El reporte debe recibir un timestamp automático

## Criterios de Aceptación
- [ ] Un usuario puede acceder al formulario desde un celular sin registrarse
- [ ] Al enviar el formulario, se crea un reporte en la base de datos encriptada
- [ ] No queda registro de IP, cookies, ni metadata del dispositivo
- [ ] El hash generado es único y no permite rastrear al reportante
- [ ] Los tests unitarios pasan al 100%
- [ ] La documentación API está generada (OpenAPI)

## Stack
- Frontend: React formulario anónimo
- Backend: FastAPI endpoint POST /api/reportes
- Base de datos: PostgreSQL tabla reportes encriptada
- Tests: pytest + TestClient

## Seguridad
- OWASP: SQL Injection (SQLAlchemy ORM), XSS (React escapa), CSRF (no aplica por ser anónimo)
- Rate limiting: máximo 5 reportes por IP por hora (solo para mitigar spam, no guardar IP permanentemente)
