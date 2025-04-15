import os

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from .Response_model import Response_profile

from ...database import get_db, User_table, Mentor_table

get_profile_router = APIRouter()

@get_profile_router.get("/user/profile", status_code=200, response_model=Response_profile)
def get_users(db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    user = db.query(User_table).filter(User_table.user_id == data["sub"]).first()

    if not user:
        return JSONResponse(status_code=404, content={"status": "User not found"})

    mentor = db.query(Mentor_table).filter(Mentor_table.user_id == user.user_id).first()

    result = \
        {
            "user_id": str(user.user_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "about": user.about,
            "contact": user.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(user.user_id)}" if user.avatar is not None else None
        }

    if mentor is not None:
        result["is_mentor"] = True

    else:
        result["is_mentor"] = False

    return result