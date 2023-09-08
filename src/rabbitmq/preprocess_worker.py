import json

from src.audio import audio
from src.rabbitmq.rabbitmq import bind_queue, connect_rabbimq


def preprocess_worker():
    """Rabbimq worker.
    Function creates connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "preprocess".

    """

    def process_link(ch, method, properties, body):
        """Downloads audio track and cuts it.
        Cut audio file is sent to exchange "processing" chat_id and
        path to cut audio with binding_key "process".
        """
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        link = data["link"]
        audio_info = audio.download_audio(link)
        file_name = audio.cut_audio(audio_info)["file_name"]
        message = {"file_name": file_name, "chat_id": chat_id}
        channel.basic_publish(
            exchange="processing", routing_key="process", body=json.dumps(message)
        )

    channel, _ = connect_rabbimq()
    channel = bind_queue(channel, process_link, "preprocess")
    channel.start_consuming()


if __name__ == "__main__":
    preprocess_worker()
