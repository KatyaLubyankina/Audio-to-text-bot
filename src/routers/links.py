from fastapi import APIRouter
from loguru import logger

from src.bot.bot import send_analytic
from src.logging import logger_wraps
from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import FileBase, LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("")
@logger_wraps()
def handle_link(request: LinkBase):
    print(f"{request.link}")
    preprocess_producer(link=request.link, chat_id=request.chat_id)
    logger.debug("process_producer finished")
    return


@router.post("/analytics")
@logger_wraps()
def analytics(request: FileBase):
    logger.debug(f"{request.path},{request.chat_id}")
    send_analytic(request.chat_id, request.path)
    return
