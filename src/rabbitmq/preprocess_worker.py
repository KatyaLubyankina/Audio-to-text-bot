import json

import pika

import src.config as config
from src.audio import audio


def preprocess_worker() -> None:
    """Rabbimq worker.
    Function creates connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "preprocess".
    Callback function downloads audio track
    from link in message (only Youtube) and cuts it.
    Then function sends to exchange "processing" chat_id and
    path to cut audio with binding_key "process".

    """
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

    binding_key = "preprocess"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        link = data["link"]
        audio_info = audio.download_audio(link)
        file_name = audio.cut_audio(audio_info)["file_name"]
        message = {"file_name": file_name, "chat_id": chat_id}
        channel.basic_publish(
            exchange="processing", routing_key="process", body=json.dumps(message)
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


preprocess_worker()
