import os
from typing import Optional, List

import jwt
from fastapi import APIRouter, Query, Header
from fastapi.params import Depends
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, User_table, Mentor_table, Admin_table

get_mentors_router = APIRouter()

@get_mentors_router.get("/admin/secreturl/mentors")
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

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    if not admin:
        return JSONResponse(status_code=403, content={"status": "Admin was not found or you are not admin"})

    query = db.query(Mentor_table).join(User_table).filter(User_table.age <= age_to, User_table.age >= age_from)

    if not direction:
        if sort_by == "name":
            if order == 'asc':
                query = query.order_by(asc(User_table.first_name), asc(User_table.last_name)).filter(User_table.age <= age_to, User_table.age >= age_from)
            else:
                query = query.order_by(desc(User_table.first_name), desc(User_table.last_name)).filter(User_table.age <= age_to, User_table.age >= age_from)
        elif sort_by == "age":
            if order == 'asc':
                query = query.order_by(asc(User_table.age)).filter(User_table.age <= age_to, User_table.age >= age_from)
            else:
                query = query.order_by(desc(User_table.age)).filter(User_table.age <= age_to, User_table.age >= age_from)
    else:
        if sort_by == "name":
            if order == 'asc':
                query = query.order_by(asc(User_table.first_name), asc(User_table.last_name)).filter(
                    User_table.age <= age_to, User_table.age >= age_from, Mentor_table.direction.in_(direction))
            else:
                query = query.order_by(desc(User_table.first_name), desc(User_table.last_name)).filter(
                    User_table.age <= age_to, User_table.age >= age_from, Mentor_table.direction.in_(direction))
        elif sort_by == "age":
            if order == 'asc':
                query = query.order_by(asc(User_table.age)).filter(User_table.age <= age_to, User_table.age >= age_from, Mentor_table.direction.in_(direction))
            else:
                query = query.order_by(desc(User_table.age)).filter(User_table.age <= age_to,
                                                                    User_table.age >= age_from, Mentor_table.direction.in_(direction))

    mentors = query.all()

    result = [
        {
            "mentor_id": str(mentor.mentor_id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "direction": mentor.direction,
            "about": user.about,
            "contact": user.contact,
            "avatar": f"https://prod-team-35-lg7sic6v.REDACTED/api/user/avatar/{str(user.user_id)}" if user.avatar is not None else None
        }
        for mentor in mentors
        for user in [db.query(User_table).filter(User_table.user_id == mentor.user_id).one()]
    ]

    return JSONResponse(status_code=200, content=result)