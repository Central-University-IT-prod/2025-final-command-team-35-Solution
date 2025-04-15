from pydantic import BaseModel

class Approve(BaseModel):
    status: bool