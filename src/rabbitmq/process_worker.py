import json

import pika


def process_worker() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "process"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        # path = data["path"]
        chat_id = data["chat_id"]
        path_to_process_file = "mock_file_process.txt"
        message = {"path": path_to_process_file, "chat_id": chat_id}
        channel.basic_publish(
            exchange="processing",
            routing_key="postprocess",
            body=json.dumps(message),
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


process_worker()
