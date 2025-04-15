import os
from uuid import UUID, uuid4

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, Mentor_table, User_table, Admin_table

delete_mentor_router = APIRouter()

@delete_mentor_router.delete("/admin/mentor/{mentor_id}")
def delete_mentor(mentor_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    if not admin:
        return JSONResponse(status_code=403, content={"status": "Admin was not found or you are not admin"})

    mentor = db.query(Mentor_table).filter(Mentor_table.mentor_id == mentor_id).first()
    if not mentor:
        return JSONResponse(status_code=404, content={"status": "Mentor not found"})

    db.delete(mentor)
    db.commit()

    return JSONResponse(status_code=200, content={"status": "Mentor deleted successfully"})
