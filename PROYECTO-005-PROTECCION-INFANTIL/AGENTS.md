# AGENTS.md — PROYECTO-005: Protección Infantil Comunitaria
# Contexto específico para Kimi Code CLI (ODIN)

## Proyecto
- Código: PROYECTO-005
- Nombre: Protección Infantil Comunitaria
- Cliente: Innovadataco (producto propio)
- Director: Jelkin Zair Carrillo Franco
- Metodología: SDD + ODIN-TRAD (app) + ODIN-IA (módulo scoring)

## Stack
- Frontend: React 19 + Vite + Tailwind + PWA
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- IA: scikit-learn / transformers
- Tests: pytest + Vitest + Playwright

## Reglas específicas de este proyecto
1. ANONIMATO ABSOLUTO: No guardar IP, cookies, metadata del reportante
2. ENCRIPTACIÓN: Todos los reportes en reposo con AES-256
3. VALIDACIÓN HUMANA: Score > 80 requiere revisión humana antes de acción
4. NO DETERMINISMO: El modelo da probabilidades, no verdades absolutas
5. EXPLICABILIDAD: Cada score debe ser explicable (SHAP values)

## Estructura SDD
- specs/001-registro-anonimo/     # Módulo 1
- specs/002-scoring-ia/             # Módulo 2 (ODIN-IA)
- specs/003-ranking-protegido/      # Módulo 3

## Comunicación con ZEUS
- ZEUS gestiona PM2 en IDC_PROYECTOS
- ODIN desarrolla código en este repo
- ZEUS valida PRs contra specs y PM2
- Jelkin aprueba merge


## Comandos de referencia
```bash
# Iniciar módulo
kimi -p "Lee specs/001-registro-anonimo/spec.md y genera plan.md y tasks.md"

# Implementar
kimi -p "Implementa las tareas de specs/001-registro-anonimo/tasks.md. Tests primero."

# Crear PR
kimi -p "Crea PR: 'Módulo Registro Anónimo - PROYECTO-005'"
```