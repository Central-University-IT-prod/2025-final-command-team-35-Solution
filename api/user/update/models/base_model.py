from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    about: Optional[str] = Field(default=None, min_length=100, max_length=2000)