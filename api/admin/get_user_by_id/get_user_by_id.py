import os
from uuid import UUID

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, User_table, Admin_table

get_user_router = APIRouter()

@get_user_router.get("/admin/secreturl/users/{user_id}")
def get_users(user_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):

    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    if not admin:
        return JSONResponse(status_code=403, content={"status": "Admin was not found or you are not admin"})

    user = db.query(User_table).filter(User_table.user_id == user_id).first()

    if not user:
        return JSONResponse(status_code=404, content={"status": "User not found"})

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

    return JSONResponse(status_code=200, content=result)