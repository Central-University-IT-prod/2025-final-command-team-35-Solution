from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    age: int = Field(ge=0, le=200)
    about: Optional[str] = Field(default=None, min_length=100, max_length=2000)
    contact: str = Field(min_length=4)
    avatar: Optional[bytes] = Field(default=None)
