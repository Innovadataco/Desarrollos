#!/usr/bin/env bash
# scripts/run-tests.sh — Ejecuta toda la batería de pruebas y genera confirmación.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPORT="$ROOT/docs/auditoria/CONFIRMACION-PRUEBAS-002.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M %Z')

mkdir -p "$(dirname "$REPORT")"

{
  echo "# CONFIRMACION-PRUEBAS-002 — Módulo 002"
  echo ""
  echo "**Fecha de ejecución:** $TIMESTAMP"
  echo "**Rama:** $(git rev-parse --abbrev-ref HEAD)"
  echo "**Commit:** $(git rev-parse HEAD)"
  echo ""
  echo "Este documento se genera automáticamente con \`scripts/run-tests.sh\`."
  echo ""

  echo "## 1. Backend tests"
  echo ""
  echo "\`\`\`"
  cd "$ROOT/src/backend"
  source .venv/bin/activate
  if pytest --cov=app --cov-report=term-missing; then
    echo "\`\`\`"
    echo ""
    echo "✅ Backend tests PASSED"
  else
    echo "\`\`\`"
    echo ""
    echo "❌ Backend tests FAILED"
    exit 1
  fi
  echo ""

  echo "## 2. Frontend unit tests"
  echo ""
  echo "\`\`\`"
  cd "$ROOT/src/frontend"
  if npm test; then
    echo "\`\`\`"
    echo ""
    echo "✅ Frontend unit tests PASSED"
  else
    echo "\`\`\`"
    echo ""
    echo "❌ Frontend unit tests FAILED"
    exit 1
  fi
  echo ""

  echo "## 3. Frontend production build"
  echo ""
  echo "\`\`\`"
  cd "$ROOT/src/frontend"
  if npm run build; then
    echo "\`\`\`"
    echo ""
    echo "✅ Production build PASSED"
  else
    echo "\`\`\`"
    echo ""
    echo "❌ Production build FAILED"
    exit 1
  fi
  echo ""

  echo "## 4. E2E tests (Playwright — chromium)"
  echo ""
  echo "\`\`\`"
  cd "$ROOT/src/frontend"
  if npm run e2e -- --project=chromium; then
    echo "\`\`\`"
    echo ""
    echo "✅ E2E tests PASSED"
  else
    echo "\`\`\`"
    echo ""
    echo "❌ E2E tests FAILED"
    exit 1
  fi
  echo ""

  echo "---"
  echo ""
  echo "> Todas las pruebas ejecutadas y confirmadas."
} > "$REPORT"

echo "Reporte generado: $REPORT"
