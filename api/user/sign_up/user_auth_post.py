import secrets
from uuid import uuid4

import bcrypt
import redis
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .models.base_model import User
from .models.response_model import Response_verify_url
from ...database import get_db, User_table, get_cache

user_auth_post_router = APIRouter()

@user_auth_post_router.post("/user/auth/sign-up", status_code=201, response_model=Response_verify_url)
def post_user(user: User, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_cache)):
    user_db = db.query(User_table).filter(User_table.login == user.login).first()
    if user_db:
        return JSONResponse(status_code=409, content={"status": "Login already exists"})

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt(rounds=4))

    new_user = User_table(
        user_id=uuid4(),
        login=user.login,
        password=hashed_password.decode(),
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        about=user.about,
        contact=user.contact,
        is_active = False,
        avatar=user.avatar
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verify_token = secrets.token_urlsafe(32)

    redis_client.set(verify_token, str(new_user.user_id))

    verify_url = f"https://prod-team-35-lg7sic6v.REDACTED/api/user/verify?token={verify_token}"
    #send_email(user.contact,
    #           "Верификация почты",
    #           f"пожалуйста подтвердите вашу почту, для этого перейдите по ссылке: {verify_url}",)

    return {"verify_url": verify_url}

