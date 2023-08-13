import pika

from src.audio import audio


def preprocess_worker() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "preprocess"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        path = audio.download_audio(body.decode())
        path_to_cut_file = audio.cut_audio(path)
        channel.basic_publish(
            exchange="processing", routing_key="process", body=path_to_cut_file
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


preprocess_worker()
