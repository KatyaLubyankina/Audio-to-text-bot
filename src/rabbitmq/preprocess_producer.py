import json

from src.logging import logger_wraps
from src.rabbitmq.rabbitmq import connect_rabbimq


@logger_wraps()
def preprocess_producer(link: str, chat_id: int) -> None:
    """Rabbitmq producer.

    Args:
        link (str): url to video file
        chat_id (int): id of telegram chat

    Function creates connection to rabbimq server and sends link and chat_id
    as a message to "processing" exchange (exchange_type="topic").
    """
    channel, connection = connect_rabbimq()
    routing_key = "preprocess"
    message = {"link": link, "chat_id": chat_id}
    channel.basic_publish(
        exchange="processing", routing_key=routing_key, body=json.dumps(message)
    )
    connection.close()
