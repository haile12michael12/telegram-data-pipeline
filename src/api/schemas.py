# telegram_api/schemas.py

from pydantic import BaseModel

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class SearchResult(BaseModel):
    message_id: int
    channel_name: str
    date: str
    message: str
