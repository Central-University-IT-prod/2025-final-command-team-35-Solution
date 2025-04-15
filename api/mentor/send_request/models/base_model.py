from typing import List

from pydantic import BaseModel, Field


class Request(BaseModel):
    about: str = Field(min_length=100, max_length=2000)
    directions: str