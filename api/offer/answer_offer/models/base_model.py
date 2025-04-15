from uuid import UUID

from pydantic import BaseModel


class Answer(BaseModel):
    status: bool