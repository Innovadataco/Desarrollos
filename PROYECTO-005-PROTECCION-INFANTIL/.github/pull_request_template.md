# Título del cambio

<!-- Usa un commit convencional: feat:, fix:, docs:, refactor:, test:, chore: -->

## Descripción

<!-- Explica qué problema resuelve o qué funcionalidad añade. -->

## Tipo de cambio

- [ ] Nueva funcionalidad
- [ ] Corrección de bug
- [ ] Refactor
- [ ] Documentación
- [ ] Tests
- [ ] Infraestructura

## Definition of Done (DoD)

- [ ] Código implementado y auto-revisado.
- [ ] Tests unitarios y/o de integración añadidos o actualizados.
- [ ] Cobertura de tests ≥ 80 % (`pytest --cov` / `vitest --coverage`).
- [ ] Linter sin advertencias (`ruff check .`, `black --check`, `npm run lint`).
- [ ] Build de producción exitoso (`docker compose build` / `npm run build`).
- [ ] Security checklist aplicada (rate limit, validación, encriptación, secrets).
- [ ] Documentación actualizada (`spec.md`, `docs/BITACORA-XXX.md`, ADR si aplica).
- [ ] Commit con mensaje convencional.
- [ ] Sin modificar archivos de `docs/auditoria/` (territorio ZEUS).

## ¿Afecta a seguridad o privacidad?

- [ ] Sí
- [ ] No

<!-- Si sí, describe el análisis de impacto. -->

## Cómo probarlo

<!-- Comandos, URLs, casos de prueba manuales. -->

## Notas para el revisor

<!-- Decisiones controvertidas, dependencias, pendientes. -->
