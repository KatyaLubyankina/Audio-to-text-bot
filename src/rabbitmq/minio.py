from minio import Minio

import src.config as config


def connect_minio():
    """Connects to MinIO server.

    Returns:
        MinIO client
    """
    minio_client = Minio(
        endpoint=f"{config.get_settings().minio_host_name}:9000",
        access_key=config.get_settings().access_key_s3,
        secret_key=config.get_settings().secret_key_s3.get_secret_value(),
        secure=False,
    )
    return minio_client
