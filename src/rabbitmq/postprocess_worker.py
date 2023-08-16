import json

import pika
import requests
from loguru import logger

import src.config as config


def postprocess_worker() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "postprocess"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        # path_to_process_file = data["path"]
        chat_id = data["chat_id"]
        postprocess_file = "mock_file_postprocess.txt"
        url = config.get_settings().url_to_sent_link + "/link/analytics"
        data = json.dumps({"chat_id": chat_id, "path": postprocess_file})
        logger.debug(f"{data}")
        requests.post(url, data=data)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


postprocess_worker()
