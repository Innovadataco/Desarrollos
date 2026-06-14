-- Migración: índices para consulta por identifier_hash (Módulo 002)
-- Aplica en PostgreSQL de producción.

CREATE INDEX IF NOT EXISTS ix_reports_identifier_hash
    ON reports (identifier_hash);

CREATE INDEX IF NOT EXISTS ix_profiles_identifier_hash
    ON profiles (identifier_hash);

-- El índice compuesto ya está declarado en el modelo Report,
-- pero se deja explícito aquí para revisiones de DBA.
CREATE INDEX IF NOT EXISTS ix_reports_identifier_reported_at
    ON reports (identifier_hash, reported_at);
