import os
from typing import Optional

import jwt
from fastapi import APIRouter, Query, Header
from fastapi.params import Depends
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List

from ...database import get_db, User_table, Mentor_table, Students_table
from .response_model import Response_student

get_students_router = APIRouter()


@get_students_router.get("/mentors/students", status_code=200, response_model=List[Response_student])
def get_mentor_students(
        db: Session = Depends(get_db),
        sort_by: Optional[str] = Query(None),
        age_from: Optional[int] = Query(0),
        age_to: Optional[int] = Query(999),
        order: Optional[str] = Query('asc'),
        authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    user_db = db.query(User_table).filter(User_table.user_id == data["sub"]).first()

    mentor_db = db.query(Mentor_table).filter(Mentor_table.user_id == user_db.user_id).first()

    if not mentor_db:
        return JSONResponse(status_code=404, content="You are not a mentor")

    students_query = (
        db.query(User_table)
        .join(Students_table, Students_table.user_id == User_table.user_id)
        .filter(Students_table.mentor_id == mentor_db.mentor_id)
        .filter(User_table.age >= age_from, User_table.age <= age_to)
    )

    # Сортировка
    if sort_by == "name":
        if order == 'asc':
            students_query = students_query.order_by(asc(User_table.first_name), asc(User_table.last_name))
        else:
            students_query = students_query.order_by(desc(User_table.first_name), desc(User_table.last_name))
    elif sort_by == "age":
        if order == 'asc':
            students_query = students_query.order_by(asc(User_table.age))
        else:
            students_query = students_query.order_by(desc(User_table.age))

    students = students_query.all()

    result = [
        {
            "user_id": str(student.user_id),
            "first_name": student.first_name,
            "last_name": student.last_name,
            "age": student.age,
            "about": student.about,
            "contact": student.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(student.user_id)}" if student.avatar is not None else None
        }
        for student in students
    ]

    return result