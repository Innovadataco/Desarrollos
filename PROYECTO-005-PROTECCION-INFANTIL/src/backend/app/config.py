import re

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.services.encryption import derive_kek


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "SemaforoConfianza"
    environment: str = "development"
    database_url: str = "sqlite:///./proteccion.db"
    report_encryption_key: str
    redis_url: str | None = None

    # Seguridad / Auth
    secret_key: str
    admin_root_password: str = "CHANGEME_ROOT_PASSWORD_2026"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 1440

    # CORS / hosts
    cors_origins: str = "http://localhost:5173,http://localhost:4173"
    allowed_hosts: str = "localhost,127.0.0.1,*.innovadataco.com"

    # Geocodificación (MaxMind GeoLite2 local, opcional)
    geolite2_path: str | None = None

    # SMTP para alertas institucionales
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "alertas@innovadataco.com"
    smtp_tls: bool = True

    @property
    def debug(self) -> bool:
        return self.environment.lower() != "production"

    def model_post_init(self, __context):
        if not self.report_encryption_key:
            raise ValueError(
                "REPORT_ENCRYPTION_KEY es requerida: debe ser 64 caracteres hexadecimales (32 bytes)."
            )
        if not re.fullmatch(r"^[0-9a-fA-F]{64}$", self.report_encryption_key):
            raise ValueError(
                "REPORT_ENCRYPTION_KEY inválida: debe ser exactamente 64 caracteres hexadecimales."
            )
        if not self.secret_key:
            raise ValueError("SECRET_KEY es requerida para JWT.")

    def encryption_kek(self) -> bytes:
        return derive_kek(self.report_encryption_key)

    def get_cors_origins(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    def get_allowed_hosts(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]


settings = Settings()
