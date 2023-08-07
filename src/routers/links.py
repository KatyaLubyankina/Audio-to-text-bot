from fastapi import APIRouter

from src.routers.schemas import LinkBase

router = APIRouter(prefix="/link", tags=["link"])


@router.post("")
def handel_link(request: LinkBase):
    return {"response": f"Processed {request.link}"}
