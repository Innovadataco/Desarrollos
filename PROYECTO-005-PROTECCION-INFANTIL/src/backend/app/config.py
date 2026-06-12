from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ProteccionInfantil"
    debug: bool = True
    database_url: str = (
        "postgresql://innovadataco:innovadataco_dev@localhost:5432/proteccion_infantil"
    )
    report_encryption_key: str = "cambia-esta-clave-por-una-de-32-bytes-hex"
    redis_url: str | None = None


settings = Settings()
