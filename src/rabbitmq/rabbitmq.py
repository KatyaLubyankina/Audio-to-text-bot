from typing import Callable

import pika

import src.config as config


def connect_rabbimq():
    """Connect to RabbitMQ.

    Connects via pika to rabbitMQ server with credentials
    and parameters from config file.
    Declares topic exchange "processing".
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
    return channel, connection


def bind_queue(
    channel: pika.channel.Channel, callback: Callable, binding_key: str
) -> pika.channel.Channel:
    """Declares queue in rabbitMQ server and binds it.

    Args:
        channel: channel for pika to communicate with RabbitMQ
        callback (Callable): function called when message is received
        binding_key (str): binding key of expected messages

    Returns:
        channel: connection channel
    """
    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue
    binding_key = binding_key

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    return channel
