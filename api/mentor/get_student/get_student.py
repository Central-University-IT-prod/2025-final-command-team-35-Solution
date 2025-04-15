import os
from uuid import UUID

import jwt
from fastapi import APIRouter, Header
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, User_table, Mentor_table, Students_table
from .response_model import Response_student

get_student_router = APIRouter()


@get_student_router.get("/mentors/students/{user_id}", status_code=200, response_model=Response_student)
def get_mentor_students(user_id: UUID, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    user_db = db.query(User_table).filter(User_table.user_id == data["sub"]).first()

    mentor_db = db.query(Mentor_table).filter(Mentor_table.user_id == user_db.user_id).first()

    if not mentor_db:
        return JSONResponse(status_code=404, content="You are not a mentor")

    student = (
        db.query(User_table)
        .join(Students_table, Students_table.user_id == User_table.user_id)
        .filter(Students_table.mentor_id == mentor_db.mentor_id, Students_table.user_id == user_id)
    ).first()

    result = \
        {
            "user_id": str(student.user_id),
            "first_name": student.first_name,
            "last_name": student.last_name,
            "age": student.age,
            "about": student.about,
            "contact": student.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(student.user_id)}" if student.avatar is not None else None
        }

    return result