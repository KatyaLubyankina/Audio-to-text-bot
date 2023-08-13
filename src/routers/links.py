from fastapi import APIRouter

from src.rabbitmq.preprocess_producer import preprocess_producer
from src.routers.schemas import LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("")
def handel_link(request: LinkBase):
    preprocess_producer(request.link)

    return {"response": f"Processed {request.link}"}
