import json

import pika

import src.config as config

# from src.audio import audio


def preprocess_worker() -> None:
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
        path_to_cut_file = "mock_path"
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        message = {"path": path_to_cut_file, "chat_id": chat_id}
        print("Preprocess_worker started as callback")
        channel.basic_publish(
            exchange="processing", routing_key="process", body=json.dumps(message)
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


preprocess_worker()
print("Started preprocess worker file")
