import json

import pika

import src.config as config
from src.logging import logger_wraps


@logger_wraps()
def preprocess_producer(link: str, chat_id: int) -> None:
    """Rabbitmq producer.

    Args:
        link (str): url to video file
        chat_id (int): id of telegram chat

    Function creates connection to rabbimq server and sends link and chat_id
    as a message to "processing" exchange(exchange_type="topic").
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

    routing_key = "preprocess"
    message = {"link": link, "chat_id": chat_id}
    channel.basic_publish(
        exchange="processing", routing_key=routing_key, body=json.dumps(message)
    )
    connection.close()
