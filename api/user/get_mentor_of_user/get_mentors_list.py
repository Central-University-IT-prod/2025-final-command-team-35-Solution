import os
from typing import Optional, List

import jwt
from fastapi import APIRouter, Query, Header
from fastapi.params import Depends
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ...database import get_db, User_table, Mentor_table, Students_table
from .response_model import Response_mentor

get_mentors_of_user_router = APIRouter()

@get_mentors_of_user_router.get("/mentors/my", status_code=200, response_model=List[Response_mentor])
def get_mentors(
    db: Session = Depends(get_db),
    sort_by: Optional[str] = Query(None),
    direction: Optional[List[str]] = Query(None),
    age_from: Optional[int] = Query(0),
    age_to: Optional[int] = Query(999),
    order: Optional[str] = Query('asc'),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])
    user_id = data["sub"]

    query = (
        db.query(Mentor_table)
        .join(Students_table, Mentor_table.mentor_id == Students_table.mentor_id)
        .join(User_table, Mentor_table.user_id == User_table.user_id)
        .filter(Students_table.user_id == user_id)  # Фильтр по user_id текущего пользователя
    )

    query = query.filter(User_table.age <= age_to, User_table.age >= age_from)

    if sort_by == "name":
        if order == 'asc':
            query = query.order_by(asc(User_table.first_name), asc(User_table.last_name))
        else:
            query = query.order_by(desc(User_table.first_name), desc(User_table.last_name))
    elif sort_by == "age":
        if order == 'asc':
            query = query.order_by(asc(User_table.age))
        else:
            query = query.order_by(desc(User_table.age))

    if direction:
        query = query.filter(Mentor_table.direction.in_(direction))

    mentors = query.all()

    result = [
        {
            "mentor_id": str(mentor.mentor_id),
            "first_name": mentor_user.first_name,
            "last_name": mentor_user.last_name,
            "age": mentor_user.age,
            "direction": mentor.direction,
            "about": mentor_user.about,
            "contact": mentor_user.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(mentor_user.user_id)}" if mentor_user.avatar is not None else None
        }
        for mentor in mentors
        for mentor_user in [db.query(User_table).filter(User_table.user_id == mentor.user_id).first()]
    ]

    return result