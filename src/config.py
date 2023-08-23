from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings.

    Attributes:
        model_config (SettingsConfigDict): path to directory with secret values
        bot_token (SecretStr): key for telegram bot
        url_app (str): url for fastapi
        end_audio_time (int): maximum duration of audio for processing
        rabbitmq_url (str): host for rabbitmq server
        rabbitmq_server (int): port for rabbitmq server
        rabbitmq_user (SecretStr): username to access rabbitmq management

    """

    model_config = SettingsConfigDict(secrets_dir="src/secrets/")
    bot_token: SecretStr
    url_app: str = "http://app:8000"
    end_of_audio_time: int = 300
    rabbitmq_url: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: SecretStr
    rabbitmq_password: SecretStr


@lru_cache()
def get_settings():
    return Settings()
