from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Offer(BaseModel):
    mentor_id: UUID
    message: Optional[str] = None