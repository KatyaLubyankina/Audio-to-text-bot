from pydantic import BaseModel


class LinkBase(BaseModel):
    chat_id: int
    link: str


class FileBase(BaseModel):
    chat_id: int
    path: str
