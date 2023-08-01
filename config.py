from functools import lru_cache
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    class Config:
        env_file = ".env_vars"
        secrets_dir = "src/secrets"


@lru_cache()
def get_settings():
    return Settings()
