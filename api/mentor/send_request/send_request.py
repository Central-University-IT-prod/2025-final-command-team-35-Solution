import datetime
import os
from uuid import uuid4

import jwt
from fastapi import APIRouter
from fastapi.params import Depends, Header
from sqlalchemy.orm import Session

from .models.base_model import Request
from .models.response_model import Response_request
from ...database import get_db, Mentors_requests_table

send_request_router = APIRouter()

@send_request_router.post("/mentors/request", status_code=201, response_model=Response_request)
def send_request(request: Request, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    new_request = Mentors_requests_table(request_id=uuid4(), user_id=data["sub"], about=request.about, direction=request.directions, date=datetime.datetime.now())

    db.add(new_request)
    db.commit()

    result = \
        {
            "request_id": f"{new_request.request_id}",
            "user_id": f"{new_request.user_id}",
            "about": new_request.about,
            "direction": new_request.direction,
            "date": new_request.date,
            "status": new_request.status if new_request.status is not None else None
        }

    return result
