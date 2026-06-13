# Estructura de Datos — Esquema SQL Completo

**Proyecto:** Semáforo de Confianza (005)  
**Fecha:** 13 de junio 2026  
**Versión:** 1.0  
**Autor:** ZEUS / ODIN  

---

## Diagrama Entidad-Relación (Texto)

```
Report (1) --- (N) Analysis
Report (N) --- (1) Profile (via identifier_hash)
Report (N) --- (N) AuditLog (via report_id)
Alert (1) --- (1) Report
Alert (1) --- (1) Institution
Digest (N) --- (1) Institution
User (1) --- (N) AuditLog (via admin_id)
User (1) --- (N) Alert (configuración)
```

---

## Tablas

### 1. `reports` — Registros Anónimos de Reportes

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador único del reporte |
| report_hash | VARCHAR(64) | NOT NULL, UNIQUE | Hash SHA-256 de confirmación para el usuario |
| reported_identifier | BYTEA | NOT NULL | Identificador encriptado (teléfono, email, @, URL) |
| description | BYTEA | NOT NULL | Descripción del incidente encriptada |
| category | VARCHAR(20) | NOT NULL | Categoría: contacto_inapropiado, solicitud_material, grooming, cita_persona, extorsion, desconocido |
| evidence_type | VARCHAR(20) | NULL | Tipo de evidencia: text, image, video, audio, screenshot, null |
| evidence_content | BYTEA | NULL | Evidencia multimedia encriptada (base64) |
| evidence_media_url | VARCHAR(255) | NULL | URL segura a archivo multimedia encriptado |
| evidence_media_path | VARCHAR(255) | NULL | Ruta en filesystem (UUID, no nombre original) |
| evidence_thumbnail_path | VARCHAR(255) | NULL | Ruta del thumbnail encriptado |
| city | VARCHAR(100) | NULL | Ciudad aproximada (si consent_location=true) |
| country | VARCHAR(100) | NULL | País (si consent_location=true) |
| consent_location | BOOLEAN | DEFAULT FALSE | ¿El usuario consintió compartir ubicación aproximada? |
| status | VARCHAR(20) | DEFAULT 'nuevo' | Estado: nuevo, en_revision, escalado, cerrado |
| score | DECIMAL(4,3) | NULL | Score de IA (0.000 - 1.000) |
| level | VARCHAR(20) | NULL | Nivel: low, medium, high, critical, severe |
| reported_at | TIMESTAMPTZ | DEFAULT NOW() | Fecha de reporte (hora truncada a franja de 6 horas) |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Última actualización |

**Índices:**
```sql
CREATE INDEX idx_reports_hash ON reports(report_hash);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_level ON reports(level);
CREATE INDEX idx_reports_category ON reports(category);
CREATE INDEX idx_reports_reported_at ON reports(reported_at);
CREATE INDEX idx_reports_score ON reports(score) WHERE score IS NOT NULL;
```

---

### 2. `analyses` — Análisis de IA (Módulo 003)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del análisis |
| report_id | UUID | NOT NULL, FK → reports(id) | Reporte analizado |
| score | DECIMAL(4,3) | NOT NULL | Score de riesgo (0.000 - 1.000) |
| level | VARCHAR(20) | NOT NULL | Nivel: low, medium, high, critical, severe |
| category | VARCHAR(20) | NOT NULL | Categoría detectada por IA |
| category_confidence | DECIMAL(4,3) | NOT NULL | Confianza de categoría (0.000 - 1.000) |
| model_version | VARCHAR(50) | NOT NULL | Versión del modelo (ej: grooming-v1.0) |
| explanation | BYTEA | NULL | SHAP values o top tokens encriptados |
| grooming_indicators | JSONB | NULL | Lista de indicadores detectados: ["secrecion", "aislamiento"] |
| description_summary | VARCHAR(200) | NULL | Resumen de 200 chars generado por IA (encriptado) |
| processed_at | TIMESTAMPTZ | DEFAULT NOW() | Cuándo se procesó |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

**Índices:**
```sql
CREATE INDEX idx_analyses_report_id ON analyses(report_id);
CREATE INDEX idx_analyses_score ON analyses(score);
CREATE INDEX idx_analyses_level ON analyses(level);
CREATE INDEX idx_analyses_category ON analyses(category);
CREATE INDEX idx_analyses_model_version ON analyses(model_version);
CREATE INDEX idx_analyses_processed_at ON analyses(processed_at);
```

---

### 3. `profiles` — Perfil de Identificador (Módulo 004)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del perfil |
| identifier_hash | VARCHAR(64) | NOT NULL, UNIQUE | Hash SHA-256 del identificador normalizado |
| identifier_type | VARCHAR(20) | NOT NULL | Tipo: phone, email, social, url, name |
| report_count | INTEGER | NOT NULL, DEFAULT 0 | Cantidad de reportes |
| score_average | DECIMAL(4,3) | NULL | Promedio de scores de análisis |
| score_max | DECIMAL(4,3) | NULL | Score máximo alcanzado |
| score_min | DECIMAL(4,3) | NULL | Score mínimo alcanzado |
| cities | JSONB | NULL | Lista de ciudades únicas: ["Bogotá", "Medellín"] |
| countries | JSONB | NULL | Lista de países únicos: ["Colombia", "México"] |
| cities_count | INTEGER | NOT NULL, DEFAULT 0 | Conteo de ciudades únicas |
| countries_count | INTEGER | NOT NULL, DEFAULT 0 | Conteo de países únicos |
| is_network | BOOLEAN | NOT NULL, DEFAULT FALSE | Flag de red organizada |
| evidence_types | JSONB | NULL | Tipos de evidencia únicos: ["image", "audio"] |
| categories | JSONB | NULL | Categorías frecuentes: [{"category": "grooming", "count": 5}] |
| first_reported_at | TIMESTAMPTZ | NULL | Primer reporte |
| last_reported_at | TIMESTAMPTZ | NULL | Último reporte |
| timeline | JSONB | NULL | Reportes por mes: [{"month": "2026-06", "count": 3, "score_avg": 0.75}] |
| network_criteria_met | JSONB | NULL | Criterios que activaron is_network: {"cities_count": true, "countries_count": true} |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Última actualización |

**Índices:**
```sql
CREATE UNIQUE INDEX idx_profiles_identifier_hash ON profiles(identifier_hash);
CREATE INDEX idx_profiles_is_network ON profiles(is_network) WHERE is_network = TRUE;
CREATE INDEX idx_profiles_score_max ON profiles(score_max);
CREATE INDEX idx_profiles_report_count ON profiles(report_count);
CREATE INDEX idx_profiles_updated_at ON profiles(updated_at);
```

---

### 4. `profile_updates` — Audit Trail de Cambios en Perfil (Módulo 004)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del update |
| profile_id | UUID | NOT NULL, FK → profiles(id) | Perfil actualizado |
| report_id | UUID | NOT NULL, FK → reports(id) | Reporte que causó el update |
| old_score_avg | DECIMAL(4,3) | NULL | Score promedio anterior |
| new_score_avg | DECIMAL(4,3) | NULL | Score promedio nuevo |
| old_score_max | DECIMAL(4,3) | NULL | Score máximo anterior |
| new_score_max | DECIMAL(4,3) | NULL | Score máximo nuevo |
| old_cities_count | INTEGER | NULL | Ciudades anterior |
| new_cities_count | INTEGER | NULL | Ciudades nuevo |
| old_countries_count | INTEGER | NULL | Países anterior |
| new_countries_count | INTEGER | NULL | Países nuevo |
| old_is_network | BOOLEAN | NULL | is_network anterior |
| new_is_network | BOOLEAN | NULL | is_network nuevo |
| triggered_network | BOOLEAN | NOT NULL, DEFAULT FALSE | Este update activó is_network |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

**Índices:**
```sql
CREATE INDEX idx_profile_updates_profile_id ON profile_updates(profile_id);
CREATE INDEX idx_profile_updates_report_id ON profile_updates(report_id);
CREATE INDEX idx_profile_updates_triggered ON profile_updates(triggered_network) WHERE triggered_network = TRUE;
CREATE INDEX idx_profile_updates_created_at ON profile_updates(created_at);
```

---

### 5. `users` — Administradores del Panel (Módulo 005)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del usuario |
| username | VARCHAR(50) | NOT NULL, UNIQUE | Nombre de usuario |
| password_hash | VARCHAR(255) | NOT NULL | Hash bcrypt (12 rounds) |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'viewer' | Rol: viewer, reviewer, supervisor, admin, root |
| two_fa_secret | VARCHAR(255) | NULL | Secret TOTP (encriptado) |
| two_fa_enabled | BOOLEAN | NOT NULL, DEFAULT FALSE | ¿2FA habilitado? |
| email | VARCHAR(255) | NULL | Email para alertas del sistema |
| phone | VARCHAR(20) | NULL | Teléfono para alertas críticas |
| active | BOOLEAN | NOT NULL, DEFAULT TRUE | ¿Activo? |
| last_login_at | TIMESTAMPTZ | NULL | Último login |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Última actualización |

**Índices:**
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(active) WHERE active = TRUE;
```

---

### 6. `audit_logs` — Audit Trail de Acciones de Admin (Módulo 005)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del log |
| user_id | UUID | NOT NULL, FK → users(id) | Admin que hizo la acción |
| action | VARCHAR(50) | NOT NULL | Acción: login, logout, view, decrypt, status_change, export, config_change |
| report_id | UUID | NULL, FK → reports(id) | Reporte afectado (nullable) |
| profile_id | UUID | NULL, FK → profiles(id) | Perfil afectado (nullable) |
| details | JSONB | NULL | Detalles: {"reason": "...", "old_status": "nuevo", "new_status": "en_revision"} |
| ip_address | VARCHAR(45) | NULL | IP del admin (IPv4 o IPv6) |
| user_agent | VARCHAR(500) | NULL | User-Agent del admin |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

**Índices:**
```sql
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_report_id ON audit_logs(report_id) WHERE report_id IS NOT NULL;
CREATE INDEX idx_audit_logs_profile_id ON audit_logs(profile_id) WHERE profile_id IS NOT NULL;
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

### 7. `alerts` — Alertas Enviadas a Instituciones (Módulo 006)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador de la alerta |
| report_id | UUID | NOT NULL, FK → reports(id) | Reporte que generó la alerta |
| institution_id | UUID | NOT NULL, FK → institutions(id) | Institución destino |
| format | VARCHAR(20) | NOT NULL | Formato: json, pdf, ncmec |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Estado: pending, delivered, failed, retrying |
| content | BYTEA | NULL | Contenido de la alerta encriptado (JSON/PDF/NCMEC) |
| sent_at | TIMESTAMPTZ | NULL | Cuándo se envió |
| delivered_at | TIMESTAMPTZ | NULL | Cuándo se confirmó entrega |
| retries | INTEGER | NOT NULL, DEFAULT 0 | Intentos de reenvío |
| error | TEXT | NULL | Error si falló |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

**Índices:**
```sql
CREATE INDEX idx_alerts_report_id ON alerts(report_id);
CREATE INDEX idx_alerts_institution_id ON alerts(institution_id);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);
```

---

### 8. `digests` — Resúmenes Periódicos (Módulo 006)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador del digest |
| period | VARCHAR(20) | NOT NULL | Período: daily, weekly, monthly |
| date | DATE | NOT NULL | Fecha del digest |
| institution_id | UUID | NOT NULL, FK → institutions(id) | Institución destino |
| report_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes incluidos |
| severe_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes severe |
| critical_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes critical |
| high_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes high |
| medium_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes medium |
| low_count | INTEGER | NOT NULL, DEFAULT 0 | Reportes low |
| network_count | INTEGER | NOT NULL, DEFAULT 0 | Redes organizadas detectadas |
| content | BYTEA | NOT NULL | Contenido del digest encriptado |
| sent_at | TIMESTAMPTZ | NULL | Cuándo se envió |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Estado: pending, delivered, failed |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |

**Índices:**
```sql
CREATE INDEX idx_digests_period_date ON digests(period, date);
CREATE INDEX idx_digests_institution_id ON digests(institution_id);
CREATE INDEX idx_digests_status ON digests(status);
```

---

### 9. `institutions` — Instituciones Conectadas (Módulo 006)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Identificador de la institución |
| name | VARCHAR(100) | NOT NULL | Nombre: ICBF, Fiscalía, Policía, NCMEC |
| code | VARCHAR(20) | NOT NULL, UNIQUE | Código: icbf, fiscalia, policia, ncmec |
| api_key_hash | VARCHAR(255) | NULL | Hash bcrypt de API key para gateway |
| contact_email | VARCHAR(255) | NOT NULL | Email para alertas |
| contact_phone | VARCHAR(20) | NULL | Teléfono para alertas críticas |
| contact_person | VARCHAR(100) | NULL | Persona de contacto |
| contract_active | BOOLEAN | NOT NULL, DEFAULT FALSE | ¿Contrato firmado? |
| contract_signed_at | DATE | NULL | Fecha de firma del contrato |
| contract_expires_at | DATE | NULL | Fecha de expiración del contrato |
| alert_config | JSONB | NOT NULL, DEFAULT '{}' | Configuración de alertas específica |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Timestamp |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Última actualización |

**Índices:**
```sql
CREATE UNIQUE INDEX idx_institutions_code ON institutions(code);
CREATE INDEX idx_institutions_contract ON institutions(contract_active) WHERE contract_active = TRUE;
```

---

### 10. `config` — Configuración del Sistema (Módulo 005, 006)

| Columna | Tipo | Constraints | Descripción |
|---------|------|-------------|-------------|
| id | INTEGER | PK, DEFAULT 1 | Singleton (solo 1 fila) |
| threshold_severe | DECIMAL(4,3) | NOT NULL, DEFAULT 0.85 | Umbral severe |
| threshold_critical | DECIMAL(4,3) | NOT NULL, DEFAULT 0.70 | Umbral critical |
| threshold_high | DECIMAL(4,3) | NOT NULL, DEFAULT 0.50 | Umbral high |
| threshold_medium | DECIMAL(4,3) | NOT NULL, DEFAULT 0.30 | Umbral medium |
| alert_severe_immediate | BOOLEAN | NOT NULL, DEFAULT TRUE | Alerta severe inmediata |
| alert_critical_4h | BOOLEAN | NOT NULL, DEFAULT TRUE | Alerta critical en 4h |
| alert_high_24h | BOOLEAN | NOT NULL, DEFAULT TRUE | Alerta high en 24h |
| alert_medium_weekly | BOOLEAN | NOT NULL, DEFAULT TRUE | Alerta medium semanal |
| alert_network_immediate | BOOLEAN | NOT NULL, DEFAULT TRUE | Alerta red inmediata (no editable) |
| digest_daily_time | TIME | NOT NULL, DEFAULT '08:00' | Hora del digest diario |
| digest_weekly_day | INTEGER | NOT NULL, DEFAULT 1 | Día del digest semanal (1=lunes) |
| digest_weekly_time | TIME | NOT NULL, DEFAULT '08:00' | Hora del digest semanal |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Última actualización |
| updated_by | UUID | NULL, FK → users(id) | Quién actualizó |

---

## SQL de Creación Completo

```sql
-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Tabla de reportes
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_hash VARCHAR(64) NOT NULL UNIQUE,
    reported_identifier BYTEA NOT NULL,
    description BYTEA NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('contacto_inapropiado', 'solicitud_material', 'grooming', 'cita_persona', 'extorsion', 'desconocido')),
    evidence_type VARCHAR(20) NULL CHECK (evidence_type IN ('text', 'image', 'video', 'audio', 'screenshot')),
    evidence_content BYTEA NULL,
    evidence_media_url VARCHAR(255) NULL,
    evidence_media_path VARCHAR(255) NULL,
    evidence_thumbnail_path VARCHAR(255) NULL,
    city VARCHAR(100) NULL,
    country VARCHAR(100) NULL,
    consent_location BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'nuevo' CHECK (status IN ('nuevo', 'en_revision', 'escalado', 'cerrado')),
    score DECIMAL(4,3) NULL CHECK (score >= 0 AND score <= 1),
    level VARCHAR(20) NULL CHECK (level IN ('low', 'medium', 'high', 'critical', 'severe')),
    reported_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reports_hash ON reports(report_hash);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_level ON reports(level);
CREATE INDEX idx_reports_category ON reports(category);
CREATE INDEX idx_reports_reported_at ON reports(reported_at);
CREATE INDEX idx_reports_score ON reports(score) WHERE score IS NOT NULL;

-- 2. Tabla de análisis de IA
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    score DECIMAL(4,3) NOT NULL CHECK (score >= 0 AND score <= 1),
    level VARCHAR(20) NOT NULL CHECK (level IN ('low', 'medium', 'high', 'critical', 'severe')),
    category VARCHAR(20) NOT NULL CHECK (category IN ('contacto_inapropiado', 'solicitud_material', 'grooming', 'cita_persona', 'extorsion', 'desconocido')),
    category_confidence DECIMAL(4,3) NOT NULL CHECK (category_confidence >= 0 AND category_confidence <= 1),
    model_version VARCHAR(50) NOT NULL,
    explanation BYTEA NULL,
    grooming_indicators JSONB NULL,
    description_summary VARCHAR(200) NULL,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_analyses_report_id ON analyses(report_id);
CREATE INDEX idx_analyses_score ON analyses(score);
CREATE INDEX idx_analyses_level ON analyses(level);
CREATE INDEX idx_analyses_category ON analyses(category);
CREATE INDEX idx_analyses_model_version ON analyses(model_version);
CREATE INDEX idx_analyses_processed_at ON analyses(processed_at);

-- 3. Tabla de perfiles
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier_hash VARCHAR(64) NOT NULL UNIQUE,
    identifier_type VARCHAR(20) NOT NULL CHECK (identifier_type IN ('phone', 'email', 'social', 'url', 'name')),
    report_count INTEGER NOT NULL DEFAULT 0,
    score_average DECIMAL(4,3) NULL,
    score_max DECIMAL(4,3) NULL,
    score_min DECIMAL(4,3) NULL,
    cities JSONB NULL,
    countries JSONB NULL,
    cities_count INTEGER NOT NULL DEFAULT 0,
    countries_count INTEGER NOT NULL DEFAULT 0,
    is_network BOOLEAN NOT NULL DEFAULT FALSE,
    evidence_types JSONB NULL,
    categories JSONB NULL,
    first_reported_at TIMESTAMPTZ NULL,
    last_reported_at TIMESTAMPTZ NULL,
    timeline JSONB NULL,
    network_criteria_met JSONB NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_profiles_is_network ON profiles(is_network) WHERE is_network = TRUE;
CREATE INDEX idx_profiles_score_max ON profiles(score_max);
CREATE INDEX idx_profiles_report_count ON profiles(report_count);
CREATE INDEX idx_profiles_updated_at ON profiles(updated_at);

-- 4. Tabla de profile updates (audit trail)
CREATE TABLE profile_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    old_score_avg DECIMAL(4,3) NULL,
    new_score_avg DECIMAL(4,3) NULL,
    old_score_max DECIMAL(4,3) NULL,
    new_score_max DECIMAL(4,3) NULL,
    old_cities_count INTEGER NULL,
    new_cities_count INTEGER NULL,
    old_countries_count INTEGER NULL,
    new_countries_count INTEGER NULL,
    old_is_network BOOLEAN NULL,
    new_is_network BOOLEAN NULL,
    triggered_network BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_profile_updates_profile_id ON profile_updates(profile_id);
CREATE INDEX idx_profile_updates_report_id ON profile_updates(report_id);
CREATE INDEX idx_profile_updates_triggered ON profile_updates(triggered_network) WHERE triggered_network = TRUE;
CREATE INDEX idx_profile_updates_created_at ON profile_updates(created_at);

-- 5. Tabla de usuarios (admin)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer' CHECK (role IN ('viewer', 'reviewer', 'supervisor', 'admin', 'root')),
    two_fa_secret VARCHAR(255) NULL,
    two_fa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    email VARCHAR(255) NULL,
    phone VARCHAR(20) NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(active) WHERE active = TRUE;

-- 6. Tabla de audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    report_id UUID NULL REFERENCES reports(id) ON DELETE SET NULL,
    profile_id UUID NULL REFERENCES profiles(id) ON DELETE SET NULL,
    details JSONB NULL,
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(500) NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_report_id ON audit_logs(report_id) WHERE report_id IS NOT NULL;
CREATE INDEX idx_audit_logs_profile_id ON audit_logs(profile_id) WHERE profile_id IS NOT NULL;
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- 7. Tabla de instituciones
CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    api_key_hash VARCHAR(255) NULL,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(20) NULL,
    contact_person VARCHAR(100) NULL,
    contract_active BOOLEAN NOT NULL DEFAULT FALSE,
    contract_signed_at DATE NULL,
    contract_expires_at DATE NULL,
    alert_config JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_institutions_contract ON institutions(contract_active) WHERE contract_active = TRUE;

-- 8. Tabla de alertas
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    format VARCHAR(20) NOT NULL CHECK (format IN ('json', 'pdf', 'ncmec')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'delivered', 'failed', 'retrying')),
    content BYTEA NULL,
    sent_at TIMESTAMPTZ NULL,
    delivered_at TIMESTAMPTZ NULL,
    retries INTEGER NOT NULL DEFAULT 0,
    error TEXT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_report_id ON alerts(report_id);
CREATE INDEX idx_alerts_institution_id ON alerts(institution_id);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);

-- 9. Tabla de digests
CREATE TABLE digests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period VARCHAR(20) NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    date DATE NOT NULL,
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    report_count INTEGER NOT NULL DEFAULT 0,
    severe_count INTEGER NOT NULL DEFAULT 0,
    critical_count INTEGER NOT NULL DEFAULT 0,
    high_count INTEGER NOT NULL DEFAULT 0,
    medium_count INTEGER NOT NULL DEFAULT 0,
    low_count INTEGER NOT NULL DEFAULT 0,
    network_count INTEGER NOT NULL DEFAULT 0,
    content BYTEA NOT NULL,
    sent_at TIMESTAMPTZ NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'delivered', 'failed')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_digests_period_date ON digests(period, date);
CREATE INDEX idx_digests_institution_id ON digests(institution_id);
CREATE INDEX idx_digests_status ON digests(status);

-- 10. Tabla de configuración
CREATE TABLE config (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    threshold_severe DECIMAL(4,3) NOT NULL DEFAULT 0.85,
    threshold_critical DECIMAL(4,3) NOT NULL DEFAULT 0.70,
    threshold_high DECIMAL(4,3) NOT NULL DEFAULT 0.50,
    threshold_medium DECIMAL(4,3) NOT NULL DEFAULT 0.30,
    alert_severe_immediate BOOLEAN NOT NULL DEFAULT TRUE,
    alert_critical_4h BOOLEAN NOT NULL DEFAULT TRUE,
    alert_high_24h BOOLEAN NOT NULL DEFAULT TRUE,
    alert_medium_weekly BOOLEAN NOT NULL DEFAULT TRUE,
    alert_network_immediate BOOLEAN NOT NULL DEFAULT TRUE,
    digest_daily_time TIME NOT NULL DEFAULT '08:00',
    digest_weekly_day INTEGER NOT NULL DEFAULT 1,
    digest_weekly_time TIME NOT NULL DEFAULT '08:00',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    updated_by UUID NULL REFERENCES users(id) ON DELETE SET NULL
);

INSERT INTO config (id) VALUES (1) ON CONFLICT DO NOTHING;

-- Seed de instituciones
INSERT INTO institutions (name, code, contact_email, alert_config) VALUES
    ('ICBF', 'icbf', 'linea141@icbf.gov.co', '{"thresholds": {"severe": true, "critical": true, "high": true, "network": true}}'),
    ('Fiscalía General', 'fiscalia', 'delitos.sexuales@fiscalia.gov.co', '{"thresholds": {"severe": true, "network": true}}'),
    ('Policía Nacional', 'policia', 'guala@policia.gov.co', '{"thresholds": {"network": true}}'),
    ('NCMEC', 'ncmec', 'cybertipline@ncmec.org', '{"thresholds": {"severe": true, "network": true}}')
ON CONFLICT (code) DO NOTHING;

-- Seed de admin root (password: cambiar inmediatamente en producción)
-- bcrypt hash de 'CHANGEME_ROOT_PASSWORD_2026'
INSERT INTO users (username, password_hash, role, email, active) VALUES
    ('root', '$2b$12$CHANGEMECHANGEMECHANGEMECHANGEMECHANGEMECHANGEME', 'root', 'admin@innovadataco.com', TRUE)
ON CONFLICT (username) DO NOTHING;
```

---

> *Documento generado por ZEUS — Innovadataco*  
> *Esquema SQL completo para PostgreSQL 16*
