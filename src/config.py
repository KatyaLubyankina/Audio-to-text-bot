from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir='src/secrets/')
    BOT_TOKEN: SecretStr


@lru_cache()
def get_settings():
    return Settings()
