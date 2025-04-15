import datetime
import os
from typing import Optional

import jwt
from fastapi import APIRouter, Query, Header
from fastapi.params import Depends
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ...database import get_db, Mentors_requests_table, Admin_table

get_requests_router = APIRouter()

@get_requests_router.get("/admin/secreturl/mentor-requests")
def get_mentor_requests(
    db: Session = Depends(get_db),
    sort_by: Optional[str] = Query(None),
    order: Optional[str] = Query('asc'),
    date_from: Optional[datetime.datetime] = Query(None),
    date_to: Optional[datetime.datetime] = Query(None),
    group_by_status: Optional[bool] = Query(False),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    admin = db.query(Admin_table).filter(Admin_table.admin_id == data["sub"]).first()

    if not admin:
        return JSONResponse(status_code=403, content={"status": "Admin was not found or you are not admin"})

    query = db.query(Mentors_requests_table)

    if date_from:
        query = query.filter(Mentors_requests_table.date >= date_from)
    if date_to:
        query = query.filter(Mentors_requests_table.date <= date_to)

    if group_by_status:
        query = query.group_by(Mentors_requests_table.status)

    if sort_by == "date":
        if order == 'asc':
            query = query.order_by(asc(Mentors_requests_table.date))
        else:
            query = query.order_by(desc(Mentors_requests_table.date))
    elif sort_by == "request_id":
        if order == 'asc':
            query = query.order_by(asc(Mentors_requests_table.request_id))
        else:
            query = query.order_by(desc(Mentors_requests_table.request_id))

    requests = query.all()

    result = [
        {
            "request_id": str(request.request_id),
            "user_id": str(request.user_id),
            "about": request.about,
            "direction": request.direction,
            "date": request.date.isoformat(),
            "status": request.status
        }
        for request in requests
    ]

    return JSONResponse(status_code=200, content=result)
