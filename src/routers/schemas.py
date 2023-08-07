from pydantic import BaseModel


class LinkBase(BaseModel):
    chat_id: int
    link: str
