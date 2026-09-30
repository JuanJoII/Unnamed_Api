from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_user: SecretStr
    postgres_password: SecretStr
    postgres_db: str
    jwt_secret_key: SecretStr
    algorithm: SecretStr
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7



settings = Settings()
