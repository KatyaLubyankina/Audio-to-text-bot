import json

import pika

import src.config as config


def process_worker() -> None:
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
