import json

import redis
import requests
from fastapi import APIRouter

import src.config as config
from src.bot.bot import send_analytic
from src.logging import logger_wraps
from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import FileBase, LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("", summary="Send link to convert audio to text")
@logger_wraps()
def handle_link(request: LinkBase) -> None:
    """Endpoint sends link and chat id to rabbitmq producer (preprocess_producer).
    Connects to Redis and search for link from request. If link was cached,
    returns uuid of transcript in MongoDB.

    Args:
    - request (LinkBase): link and chat_id.
    """
    redis_client = redis.Redis(host="redis")
    cache_value = redis_client.get(request.link)
    if cache_value is not None:
        url = config.get_settings().url_app + "/link/analytics"
        data = json.dumps(
            {"chat_id": request.chat_id, "file_uuid": str(cache_value.decode("utf-8"))}
        )
        requests.post(url, data=data)
    else:
        preprocess_producer(link=request.link, chat_id=request.chat_id)


@router.post("/analytics", summary="Send analytics on video to user")
@logger_wraps()
def analytics(request: FileBase):
    """Endpoint sends analytics to send_analytic function.

    Args:
    - request (FileBase): contains chat id and uuid for file in MongoDB.
    """
    send_analytic(chat_id=request.chat_id, file_uuid=request.file_uuid)
    return
