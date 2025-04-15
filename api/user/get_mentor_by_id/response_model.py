from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Response_mentor(BaseModel):
    mentor_id: UUID
    first_name: str
    last_name: str
    age: int
    direction: str
    about: str
    contact: str
    avatar: Optional[str]