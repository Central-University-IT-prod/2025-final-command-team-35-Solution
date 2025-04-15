import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.database import get_db, User_table
from .models.base_model import User
from .models.response_model import Response_user_token

user_auth_sign_in_router = APIRouter()

@user_auth_sign_in_router.post("/user/auth/sign-in", status_code=200, response_model=Response_user_token)
def post_user(user: User, db: Session = Depends(get_db)):
    user_db = db.query(User_table).filter_by(login=user.login, is_active=True).first()

    if not user_db:
        return JSONResponse(status_code=404, content={"status": "User was not found"})

    if not(bcrypt.checkpw(user.password.encode("utf-8"), user_db.password.encode("utf-8"))):
        return JSONResponse(status_code=404, content={"status": "Invalid password"})

    token_payload = {
        "sub": str(user_db.user_id),
        "exp": datetime.utcnow() + timedelta(days=365)
    }
    token = jwt.encode(token_payload, os.getenv("RANDOM_SECRET"), algorithm='HS256')

    return {"token": token}

