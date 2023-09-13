import json

import redis
import requests

import src.config as config
from src.logging import logger_wraps
from src.rabbitmq.rabbitmq import bind_queue, connect_rabbimq


def put_doc_to_redis(link: str, uid: str):
    """Adds pair link-uuid to Redis.

    Args:
        link (str): link to Youtube video.
        uid (str): uuid of file in MongoDB.
    """
    redis_client = redis.Redis(host="redis")
    redis_client.set(link, uid)


@logger_wraps()
def postprocess_worker():
    """Rabbitmq worker.
    Function gets connection to rabbimq server and consumes messages
    from topic exchange "processing" with routing_key "postprocess".
    Callback function handles text postprocessing.
    Then function sends chat id and uuid of file
    to exchange "processing" with binding_key "postprocess".
    """

    def postprocess(ch, method, properties, body):
        """Postprocess of audio file.
        Sends request to /link/analytics FastAPI endpoint with chat id and
        uuid of file in MongoDB.
        Puts pair link to video - uuid to Redis for cashing.
        """
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        file_uuid_mongo = data["file_uuid"]
        link = data["link"]
        put_doc_to_redis(link, file_uuid_mongo)
        url = config.get_settings().url_app + "/link/analytics"
        request = json.dumps({"chat_id": chat_id, "file_uuid": file_uuid_mongo})
        requests.post(url, data=request)

    channel, _ = connect_rabbimq()
    channel = bind_queue(channel, postprocess, "postprocess")
    channel.start_consuming()


if __name__ == "__main__":
    postprocess_worker()
