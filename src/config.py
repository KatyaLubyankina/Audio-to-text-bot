from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="src/secrets/")
    bot_token: SecretStr
    url_to_sent_link: str = "http://app:8000"
    end_of_audio_time: int = 300
    rabbitmq_url: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: SecretStr
    rabbitmq_password: SecretStr


@lru_cache()
def get_settings():
    return Settings()
