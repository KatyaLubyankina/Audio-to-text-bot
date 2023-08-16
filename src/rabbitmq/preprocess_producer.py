import json

import pika


def preprocess_producer(link: str, chat_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    routing_key = "preprocess"
    message = {"link": link, "chat_id": chat_id}
    channel.basic_publish(
        exchange="processing", routing_key=routing_key, body=json.dumps(message)
    )
    connection.close()
