import datetime
import os
from uuid import uuid4

import jwt
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .models.base_model import Offer
from .models.response_model import Response_offer
from ...database import get_db, User_table, Offer_table, Mentor_table

post_offer_router = APIRouter()

@post_offer_router.post("/mentors/offer", status_code=201, response_model=Response_offer)
def post_offer(offer: Offer, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    data = jwt.decode(token, os.getenv("RANDOM_SECRET"), algorithms=['HS256'])

    user = db.query(User_table).filter(User_table.user_id == data["sub"]).first()
    mentor = db.query(Mentor_table).join(User_table).filter(Mentor_table.mentor_id == offer.mentor_id, User_table.user_id == Mentor_table.user_id).first()

    new_offer = Offer_table(offer_id=uuid4(), mentor_id=mentor.mentor_id, user_id=user.user_id, message=offer.message, date=datetime.datetime.now())

    db.add(new_offer)
    db.commit()

    mentor_contact = db.query(User_table).filter(User_table.user_id == mentor.user_id).first()

    # send_email("New offer", f"You have received an offer from {user.contact}", mentor_contact.contact)

    result = \
        {
            "offer_id": f"{new_offer.offer_id}",
            "mentor_id": f"{new_offer.mentor_id}",
            "user_id": f"{new_offer.user_id}",
            "message": f"{new_offer.message}",
            "date": new_offer.date
        }

    return result
