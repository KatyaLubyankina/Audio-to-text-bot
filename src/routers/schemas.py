from pydantic import BaseModel


class LinkBase(BaseModel):
    """Schema for link for processing."""

    chat_id: int
    link: str


class FileBase(BaseModel):
    """Schema for file with analytics."""

    chat_id: int
    path: str
