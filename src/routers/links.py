from fastapi import APIRouter

from src.bot.bot import send_analytic
from src.logging import logger_wraps
from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import FileBase, LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("", summary="Send link to convert audio to text")
@logger_wraps()
def handle_link(request: LinkBase) -> None:
    """Endpoint sends link and chat id to rabbitmq producer (preprocess_producer).

    Args:
    - request (LinkBase): link and chat_id.
    """
    preprocess_producer(link=request.link, chat_id=request.chat_id)


@router.post("/analytics", summary="Send analytics on video to user")
@logger_wraps()
def analytics(request: FileBase):
    """Endpoint sends analytics to send_analytic function.

    Args:
    - request (FileBase): contains chat id and uuid for file in MongoDB.
    """
    send_analytic(request.chat_id, request.file_uuid)
    return
