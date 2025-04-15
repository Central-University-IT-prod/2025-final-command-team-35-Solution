from pydantic import BaseModel

class Response_user_token(BaseModel):
    token: str