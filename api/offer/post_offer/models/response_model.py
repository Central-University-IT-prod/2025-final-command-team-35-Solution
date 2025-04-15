import datetime

from pydantic import BaseModel
from uuid import UUID

class Response_offer(BaseModel):
    offer_id: UUID
    mentor_id: UUID
    user_id: UUID
    message: str
    date: datetime.datetime