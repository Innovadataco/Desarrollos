# Security Checklist — Innovadataco
**Versión:** 1.0.0  
**Basado en:** OWASP Top 10 2021 + CIS Controls  
**Responsable:** ODIN (implementa) + ZEUS (audita)  
**Frecuencia:** Cada release + Cada cambio de arquitectura

---

## 1. PRE-DEPLOY (Obligatorio)

### 1.1 Secrets y Configuración
- [ ] Ningún secret hardcodeado en código
- [ ] Variables de entorno en `.env.example` (sin valores reales)
- [ ] `.env` en `.gitignore`
- [ ] Secrets rotados si hubo leak
- [ ] Claves de encriptación >= 256 bits (32 bytes)

### 1.2 Dependencias
- [ ] `npm audit` — 0 vulnerabilidades críticas
- [ ] `pip-audit` — 0 vulnerabilidades críticas
- [ ] Dependencias actualizadas (no más de 2 versiones atrás)
- [ ] No hay dependencias abandonadas (check en npm/pypi)

### 1.3 Autenticación y Autorización
- [ ] Passwords hasheados con bcrypt/Argon2 (no MD5, no SHA1)
- [ ] JWT con expiración corta (< 24h) + refresh tokens
- [ ] Rate limiting en login (5 intentos / 15 min)
- [ ] 2FA disponible para admins
- [ ] RBAC implementado (roles: admin, user, auditor)
- [ ] No hay endpoints sin auth que deberían tener auth

### 1.4 Inputs y Validación
- [ ] Todos los inputs validados (Pydantic / Zod / class-validator)
- [ ] SQL Injection: ORM parametrizado, no concatenación
- [ ] XSS: React escapa automático, o sanitización backend
- [ ] CSRF: Tokens en formularios POST
- [ ] File upload: Validar tipo, tamaño, escanear virus
- [ ] No SSRF (Server-Side Request Forgery): Validar URLs externas

### 1.5 Encriptación
- [ ] TLS 1.3 en tránsito (certificado válido, no auto-firmado en prod)
- [ ] AES-256-GCM en reposo para datos sensibles
- [ ] KEK derivada de master key (no master key directamente)
- [ ] DEK aleatoria por registro (no reutilizar)
- [ ] IV único por operación de encriptación

### 1.6 Headers y Configuración
- [ ] HSTS habilitado
- [ ] Content-Security-Policy (CSP) configurado
- [ ] X-Frame-Options: DENY o SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] Permissions-Policy configurado
- [ ] CORS configurado (no `*` en producción)

---

## 2. POST-DEPLOY (Monitoreo)

### 2.1 Logging y Auditoría
- [ ] Logs de autenticación (login exitoso/fallido)
- [ ] Logs de cambios críticos (delete, update masivo)
- [ ] Logs sin datos sensibles (no loggear passwords, tokens, PII)
- [ ] Retención de logs: mínimo 90 días
- [ ] Alertas automáticas para eventos sospechosos

### 2.2 Monitoreo de Seguridad
- [ ] Alerta si rate limit se dispara (> 100 bloqueos / hora)
- [ ] Alerta si JWT inválidos > 50 / hora
- [ ] Alerta si errores 500 > 10 / hora
- [ ] Alerta si CPU / RAM anormales
- [ ] Escaneo de vulnerabilidades semanal (Dependabot, Snyk)

### 2.3 Backup y Recuperación
- [ ] Backup diario de BD automatizado
- [ ] Backup encriptado (AES-256)
- [ ] Test de restauración mensual
- [ ] RTO < 4 horas, RPO < 1 hora

---

## 3. ESPECÍFICO POR PROYECTO

### Proyecto 005 (Protección Infantil)
- [ ] No se guarda IP del reportante
- [ ] No se guarda user-agent
- [ ] No se usan cookies de tracking
- [ ] No se guarda metadata del navegador
- [ ] Reportes encriptados en reposo (AES-256-GCM)
- [ ] Hash único por reporte (SHA-256 + nonce)
- [ ] Rate limiting: 5 reportes / hora / IP
- [ ] No hay endpoint para listar todos los reportes (solo crear)
- [ ] Validación de inputs estricta (longitudes, caracteres permitidos)
- [ ] Sanitización de evidencias (no ejecutar contenido como código)

---

## 4. HERRAMIENTAS RECOMENDADAS

| Herramienta | Uso | Frecuencia |
|-------------|-----|------------|
| `npm audit` | Vulnerabilidades JS | Cada build |
| `pip-audit` | Vulnerabilidades Python | Cada build |
| `ruff check` | Linter Python | Cada commit |
| `black` | Formato Python | Cada commit |
| `OWASP ZAP` | Pentest web | Cada release |
| `GitHub Dependabot` | Alertas de dependencias | Continuo |
| `Snyk` | Escaneo de vulnerabilidades | Semanal |

---

> "La seguridad no es un feature, es la base. Sin seguridad, no hay deploy."
> **Security Checklist — Innovadataco**
