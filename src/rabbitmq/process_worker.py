import json
import os

from src.rabbitmq.minio import connect_minio
from src.rabbitmq.mongo import add_document_mongo
from src.rabbitmq.rabbitmq import bind_queue, connect_rabbimq
from src.whisper.whisper_transcribe import transcribe_text


def process_worker():
    """Rabbimq worker.
    Function gets connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "process".
    """

    def get_transcript(ch, method, properties, body):
        """Processes audio file.
        Gets connection to MinIO to get audio file via connect_minio function.
        Transcribes audio via Whisper model (transcribe_text function).
        Sends message to "processing" exchange with key="postprocess".
        """
        data = json.loads(body.decode())
        file_name = data["file_name"]
        minio_client = connect_minio()
        minio_client.fget_object("audio", file_name, f"src/rabbitmq/{file_name}")
        audio_bytes = open(f"src/rabbitmq/{file_name}", "rb")
        transcribe_text(audio_bytes, "src/rabbitmq/transcribed_text.txt")
        audio_bytes.close()
        uuid = add_document_mongo("src/rabbitmq/transcribed_text.txt")
        os.remove(f"src/rabbitmq/{file_name}")
        chat_id = data["chat_id"]
        message = {"file_uuid": uuid, "chat_id": chat_id}
        channel.basic_publish(
            exchange="processing",
            routing_key="postprocess",
            body=json.dumps(message),
        )

    channel, _ = connect_rabbimq()
    channel = bind_queue(channel, get_transcript, "process")
    channel.start_consuming()


if __name__ == "__main__":
    process_worker()
