from typing import Optional
from pydantic import Field
from pydantic import BaseModel
from uuid import UUID

class Response_offer(BaseModel):
    student_id: UUID
    user_id: UUID
    mentor_id: UUID