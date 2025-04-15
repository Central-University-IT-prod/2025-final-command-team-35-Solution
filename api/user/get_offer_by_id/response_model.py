import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Response_offer(BaseModel):
    mentor_id: UUID
    user_id: UUID
    message: Optional[str]
    status: bool
    date: datetime.datetime