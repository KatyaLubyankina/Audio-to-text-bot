import json

import pika
import requests

import src.config as config
from src.logging import logger_wraps


@logger_wraps()
def postprocess_worker():
    """Rabbitmq worker.
    Function creates connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "postprocess".
    Callback function handles text postprocessing.
    Then function sends chat id and path to post_process file
    to exchange "processing" with binding_key "postprocess".

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

    binding_key = "postprocess"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        postprocess_file = "mock_file_postprocess.txt"
        url = config.get_settings().url_app + "/link/analytics"
        data = json.dumps({"chat_id": chat_id, "path": postprocess_file})
        requests.post(url, data=data)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    postprocess_worker()
