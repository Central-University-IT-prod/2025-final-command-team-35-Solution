from pydantic import BaseModel

class Mentor(BaseModel):
    direction: str
    about: str