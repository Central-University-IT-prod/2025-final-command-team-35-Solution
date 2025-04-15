import os
from uuid import UUID, uuid4

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .base_model import Approve
from ...database import get_db, Mentors_requests_table, Mentor_table, User_table, Admin_table

approve_router = APIRouter()

@approve_router.post("/admin/secreturl/mentor-requests/{request_id}")
def approve_request(approve: Approve, request_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    if not admin:
        return JSONResponse(status_code=403, content={"status": "Admin was not found or you are not admin"})

    request = db.query(Mentors_requests_table).filter(Mentors_requests_table.request_id == request_id).first()

    if not request:
        return JSONResponse(status_code=404, content={"status": "Request not found"})

    if approve.status:
        request.status = True

        user = db.query(User_table).filter(User_table.user_id == request.user_id).first()

        new_mentor = Mentor_table(mentor_id=uuid4(), user_id=request.user_id, direction=request.direction)

        db.add(new_mentor)
        db.commit()

        # send_email(user.contact, "Approve", f"Your request has been approved, your id: {new_mentor.mentor_id}")

    else:
        request.status = False

        user = db.query(User_table).filter(User_table.user_id == request.user_id).first()

        # send_email(user.contact, "Approve", "Sorry but your request has not approved")

        db.commit()
