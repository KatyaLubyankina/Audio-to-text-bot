import json

import pika
import redis
import requests

import src.config as config
from src.logging import logger_wraps
from src.rabbitmq.rabbitmq import bind_queue, connect_rabbimq


def put_doc_to_redis(link: str, id: str):
    """Adds pair link-id to Redis.

    Args:
        link (str): link to Youtube video.
        id (str): uuid of file in CouchDB.
    """
    redis_client = redis.Redis(host="redis")
    redis_client.set(link, id)


@logger_wraps()
def postprocess_worker():
    """Rabbitmq worker.
    Function gets connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "postprocess".
    Callback function handles text postprocessing.
    Then function sends chat id and uuid of file
    to exchange "processing" with binding_key "postprocess".
    """

    def postprocess(
        channel: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ):
        """Postprocess of audio file.
        Sends request to /link/analytics FastAPI endpoint with chat id and
        uuid of file in MongoDB.
        Puts pair link to video - uuid to Redis for cashing.
        """
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        id = data["id"]
        link = data["link"]
        put_doc_to_redis(link, id)
        url = config.get_settings().url_app + "/link/analytics"
        request = json.dumps({"chat_id": chat_id, "file_id": id})
        requests.post(url, data=request)

    channel, _ = connect_rabbimq()
    channel = bind_queue(channel, postprocess, "postprocess")
    channel.start_consuming()


if __name__ == "__main__":
    postprocess_worker()
