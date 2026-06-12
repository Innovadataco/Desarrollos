import re

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ProteccionInfantil"
    environment: str = "development"
    database_url: str = "sqlite:///./proteccion.db"
    report_encryption_key: str
    redis_url: str | None = None

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


settings = Settings()
