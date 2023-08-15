import pika


def postprocess_worker() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="processing", exchange_type="topic")

    result = channel.queue_declare("", exclusive=True)
    queue_name = result.method.queue

    binding_key = "postprocess"

    channel.queue_bind(exchange="processing", queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        proccesed_text = body.decode()
        print(proccesed_text)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


postprocess_worker()
