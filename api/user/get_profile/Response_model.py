from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Response_profile(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    age: int
    about: Optional[str]
    contact: str
    avatar: Optional[str]
    is_mentor: bool