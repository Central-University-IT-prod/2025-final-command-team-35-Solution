from pydantic import BaseModel
from uuid import UUID

class Response_student(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    age: int
    about: str
    contact: str
    avatar: str