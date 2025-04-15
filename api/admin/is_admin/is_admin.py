import os

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ...database import get_db, Admin_table

is_admin_router = APIRouter()

@is_admin_router.post("/check")
def crete_mentor(db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    return True if admin is not None else False