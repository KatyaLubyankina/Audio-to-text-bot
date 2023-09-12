import json

import requests

import src.config as config
from src.logging import logger_wraps
from src.rabbitmq.rabbitmq import bind_queue, connect_rabbimq


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
        """
        data = json.loads(body.decode())
        chat_id = data["chat_id"]
        file_uuid_mongo = data["file_uuid"]
        url = config.get_settings().url_app + "/link/analytics"
        data = json.dumps({"chat_id": chat_id, "file_uuid": file_uuid_mongo})
        requests.post(url, data=data)

    channel, _ = connect_rabbimq()
    channel = bind_queue(channel, postprocess, "postprocess")
    channel.start_consuming()


if __name__ == "__main__":
    postprocess_worker()
