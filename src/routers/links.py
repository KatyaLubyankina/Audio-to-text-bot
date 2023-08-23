from fastapi import APIRouter

from src.bot.bot import send_analytic
from src.logging import logger_wraps
from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import FileBase, LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("")
@logger_wraps()
def handle_link(request: LinkBase) -> None:
    """Endpoint sends link and chat id to rabbitmq producer (preprocess_producer).

    Args:
        request (LinkBase): link and chat_id.
    """
    preprocess_producer(link=request.link, chat_id=request.chat_id)


@router.post("/analytics")
@logger_wraps()
def analytics(request: FileBase):
    """Endpoint sends analytic to send_analytic function.

    Args:
        request (FileBase): _description_
    """
    send_analytic(request.chat_id, request.path)
    return
