from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Response_user_update(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    age: int
    about: Optional[str]
    contact: Optional[str]