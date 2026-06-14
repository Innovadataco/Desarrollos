# CONFIRMACION-PRUEBAS-002 — Módulo 002

**Fecha de ejecución:** 2026-06-13 23:03 -05
**Rama:** feature/v2-fullstack
**Commit:** 4f494b0b014f669bfbcbad0dd48b667ea6e7be01

Este documento se genera automáticamente con `scripts/run-tests.sh`.

## 1. Backend tests

```
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/innovadataco/Documents/GitHub/Desarrollos/PROYECTO-005-PROTECCION-INFANTIL/src/backend
plugins: Faker-37.2.0, cov-7.1.0, asyncio-1.4.0, anyio-4.13.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 123 items

tests/test_admin.py .....                                                [  4%]
tests/test_admin_digest.py ..                                            [  5%]
tests/test_admin_export.py ........                                      [ 12%]
tests/test_alertas.py ....                                               [ 15%]
tests/test_analyze.py ....                                               [ 18%]
tests/test_auth.py ..                                                    [ 20%]
tests/test_cache.py ...                                                  [ 22%]
tests/test_config.py ....                                                [ 26%]
tests/test_consultas.py ................                                 [ 39%]
tests/test_email_service.py ....                                         [ 42%]
tests/test_encryption.py ....                                            [ 45%]
tests/test_evidence.py ......                                            [ 50%]
tests/test_gateway.py .........                                          [ 57%]
tests/test_ia_audit.py ....                                              [ 60%]
tests/test_identifier.py ...........                                     [ 69%]
tests/test_profiles.py .....                                             [ 73%]
tests/test_reportes.py ....................                              [ 90%]
tests/test_resources.py ..                                               [ 91%]
tests/test_security.py ......                                            [ 96%]
tests/test_totp.py ....                                                  [100%]

================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.5-final-0 _______________

Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
app/__init__.py                        0      0   100%
app/config.py                         38      1    97%   52
app/database.py                       21      5    76%   25-29, 33
app/main.py                           48      7    85%   28-30, 66, 74-75, 98
app/models.py                        181      0   100%
app/routers/__init__.py                0      0   100%
app/routers/admin/__init__.py         27      0   100%
app/routers/admin/alerts.py           11      2    82%   19-20
app/routers/admin/analytics.py        25      4    84%   45-53
app/routers/admin/audit.py            13      0   100%
app/routers/admin/config.py           40      0   100%
app/routers/admin/digest.py           19      0   100%
app/routers/admin/profiles.py         40      3    92%   56, 81, 97
app/routers/admin/reports.py          89     21    76%   45, 47, 49, 51, 53, 89, 116-133, 164, 171, 205
app/routers/admin/users.py            42     12    71%   22-23, 33-48, 70
app/routers/alertas.py                37      1    97%   27
app/routers/analyze.py                39      9    77%   53-65, 78
app/routers/consultas.py              74      2    97%   17, 102
app/routers/evidence.py               43      5    88%   64, 88, 100-101, 104
app/routers/gateway.py                73      4    95%   34, 145, 172, 193
app/routers/reportes.py               91      3    97%   43, 184-185
app/routers/resources.py              21      0   100%
app/schemas.py                        85      0   100%
app/services/__init__.py               0      0   100%
app/services/analysis_service.py      23      0   100%
app/services/auth.py                  46      5    89%   50-52, 54, 60
app/services/cache_service.py         51     16    69%   16, 19-26, 37-40, 58-59, 68-69
app/services/email_service.py         51     15    71%   21-38, 78, 105-108
app/services/encryption.py            71      6    92%   14, 31, 53, 77, 96, 115
app/services/evidence_service.py     101     16    84%   66-71, 81-85, 127, 145-148, 167
app/services/export_service.py        55      1    98%   41
app/services/ia_audit_service.py      25      0   100%
app/services/identifier.py            47      0   100%
app/services/profile_service.py       73      2    97%   25, 28
app/services/rate_limit.py            89     22    75%   32-37, 43, 74-75, 88-91, 107-110, 120, 125, 151-153
app/services/scoring.py               65     17    74%   47-48, 62-74, 93, 95
app/services/totp_service.py          38      5    87%   38, 60-63
app/utils/__init__.py                  0      0   100%
app/utils/category.py                  6      1    83%   20
app/utils/time.py                      7      1    86%   11
----------------------------------------------------------------
TOTAL                               1805    186    90%
============================= 123 passed in 15.96s =============================
```

✅ Backend tests PASSED

## 2. Frontend unit tests

```

> proteccion-infantil-frontend@1.0.0 test
> vitest run


 RUN  v3.2.6 /Users/innovadataco/Documents/GitHub/Desarrollos/PROYECTO-005-PROTECCION-INFANTIL/src/frontend

 ✓ src/components/SearchView.test.jsx (4 tests) 98ms
 ✓ src/components/ReportForm.test.jsx (6 tests) 129ms

 Test Files  2 passed (2)
      Tests  10 passed (10)
   Start at  23:03:54
   Duration  621ms (transform 50ms, setup 45ms, collect 124ms, tests 227ms, environment 297ms, prepare 69ms)

```

✅ Frontend unit tests PASSED

## 3. Frontend production build

```

> proteccion-infantil-frontend@1.0.0 build
> vite build

vite v6.4.3 building for production...
transforming...
✓ 46 modules transformed.
rendering chunks...
computing gzip size...
dist/registerSW.js                0.13 kB
dist/index.html                   0.65 kB │ gzip:  0.38 kB
dist/assets/index-43GGPf3H.css   15.96 kB │ gzip:  3.75 kB
dist/assets/index-Ds6sAxdi.js   256.69 kB │ gzip: 81.44 kB
✓ built in 594ms

PWA v0.21.2
mode      generateSW
precache  6 entries (269.68 KiB)
files generated
  dist/sw.js
  dist/workbox-9c191d2f.js
```

✅ Production build PASSED

## 4. E2E tests (Playwright — chromium)

```

> proteccion-infantil-frontend@1.0.0 e2e
> playwright test --project=chromium


Running 6 tests using 6 workers

  ✓  5 [chromium] › tests/e2e/smoke.spec.js:4:3 › Smoke tests › la página carga y muestra el formulario de búsqueda (181ms)
  ✓  3 [chromium] › tests/e2e/smoke.spec.js:11:3 › Smoke tests › se puede navegar entre las tres pestañas (415ms)
  ✓  2 [chromium] › tests/e2e/report-form.spec.js:3:1 › el wizard de reporte avanza por los 4 pasos (534ms)
  ✓  4 [chromium] › tests/e2e/report-form.spec.js:34:1 › se puede reportar un email y adjuntar una imagen (639ms)
  ✓  1 [chromium] › tests/e2e/consulta-reporte.spec.js:4:3 › Flujo consulta + reporte › consulta un identificador sin reportes, lo reporta y muestra confirmación (1.4s)
  ✓  6 [chromium] › tests/e2e/demo-tasks-002.spec.js:8:1 › recorrido visual de todas las tasks del Módulo 002 (24.7s)

  6 passed (26.0s)
```

✅ E2E tests PASSED

---

> Todas las pruebas ejecutadas y confirmadas.
