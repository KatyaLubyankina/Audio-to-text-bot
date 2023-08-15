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
        path = body.decode()
        print(path)
        channel.basic_publish(
            exchange="processing",
            routing_key="postprocess",
            body="moc_file_process.txt",
        )

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


process_worker()
