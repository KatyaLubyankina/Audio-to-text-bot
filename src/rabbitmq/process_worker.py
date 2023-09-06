import json
import os

import pika
from minio import Minio

import src.config as config
from src.whisper.whisper_transcribe import transcribe_text


def process_worker():
    """Rabbimq worker.
    Function creates connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "process".
    Callback function processes audio.
    Then function sends chat id and path to process file
    to exchange "processing" with binding_key "postprocess".

    """
    print("process worker started")
    username = config.get_settings().rabbitmq_user.get_secret_value()
    password = config.get_settings().rabbitmq_password.get_secret_value()
    credentials = pika.PlainCredentials(username, password)
    host = config.get_settings().rabbitmq_url
    port = config.get_settings().rabbitmq_port
    parameters = pika.ConnectionParameters(
        host, port, "/", credentials=credentials, retry_delay=5
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "process"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        file_name = data["file_name"]
        minio_client = Minio(
            endpoint=f"{config.get_settings().minio_host_name}:9000",
            access_key=config.get_settings().access_key_s3,
            secret_key=config.get_settings().secret_key_s3.get_secret_value(),
            secure=False,
        )
        minio_client.fget_object("audio", file_name, f"src/rabbitmq/{file_name}")
        audio_bytes = open(f"src/rabbitmq/{file_name}", "rb")
        transcribe_text(audio_bytes, "src/rabbitmq/transcribed_text.txt")
        audio_bytes.close()
        os.remove(f"src/rabbitmq/{file_name}")
        chat_id = data["chat_id"]
        path_to_process_file = "src/rabbitmq/transcribed_text.txt"
        message = {"path": path_to_process_file, "chat_id": chat_id}
        channel.basic_publish(
            exchange="processing",
            routing_key="postprocess",
            body=json.dumps(message),
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    process_worker()
