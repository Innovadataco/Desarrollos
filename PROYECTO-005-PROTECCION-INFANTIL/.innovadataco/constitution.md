# Constitution — PROYECTO-005: Protección Infantil

## Principios
1. La seguridad y anonimato del reportante es prioridad absoluta
2. El modelo de IA es una herramienta de apoyo, no una sentencia
3. Toda funcionalidad debe ser testeada antes de mergear
4. La documentación se genera con el código, no después
5. Cada decisión arquitectónica se documenta en un ADR

## Calidad
- Cobertura de tests mínima: 80%
- Tiempo de respuesta API: < 200ms
- Disponibilidad: 99.9%

## Stack aprobado
- Frontend: React 19 + Vite + Tailwind
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- IA: scikit-learn / transformers
- DevOps: Docker + GitHub Actions

## Seguridad
- OWASP Top 10 compliance
- Encriptación end-to-end
- No secrets en código (usar .env)
- Rate limiting en APIs

## Gobernanza
- Jelkin aprueba specs y merges
- ZEUS valida PRs contra PM2
- ODIN ejecuta desarrollo y tests
