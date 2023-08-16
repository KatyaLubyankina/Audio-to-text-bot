from fastapi import APIRouter
from loguru import logger

from src.bot.bot import send_analytic
from src.logging import logger_wraps
from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("")
def handle_link(request: LinkBase):
    preprocess_producer(request.link, request.chat_id)

    return


@router.post("/analytics")
@logger_wraps()
def analytics(path: str, chat_id: int):
    logger.debug(f"{path},{chat_id}")
    send_analytic(chat_id, path)
    return
