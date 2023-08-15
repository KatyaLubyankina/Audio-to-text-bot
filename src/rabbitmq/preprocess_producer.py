import pika


def preprocess_producer(link):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    routing_key = "preprocess"
    channel.basic_publish(exchange="processing", routing_key=routing_key, body=link)
    connection.close()
