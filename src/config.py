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
        mongo_username (SecretStr): username to access MongoDB
        mongo_password (SecretStr): password to access MongoDB
        cluster (SecretStr): name of cluster in MongoDB

    """

    model_config = SettingsConfigDict(secrets_dir="src/secrets/")
    bot_token: SecretStr = ""
    url_app: str = "http://app:8000"
    end_of_audio_time: int = 100
    rabbitmq_url: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: SecretStr
    rabbitmq_password: SecretStr
    minio_host_name: str = "minio"
    access_key_s3: str = "minioadmin"
    secret_key_s3: SecretStr
    rabbitmq_user: SecretStr = "guest"
    rabbitmq_password: SecretStr = "guest"
    mongo_username: SecretStr
    mongo_password: SecretStr
    cluster: SecretStr


@lru_cache()
def get_settings():
    return Settings()
