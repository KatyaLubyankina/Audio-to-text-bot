from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="src/secrets/")
    BOT_TOKEN: SecretStr
    url_to_sent_link: str = "http://localhost:8000/link"
    end_of_audio_time: int = 300


@lru_cache()
def get_settings():
    return Settings()
